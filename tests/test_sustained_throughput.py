import asyncio
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_sustained_throughput as r


def row(uid='a', start=1.1, elapsed=.1, correct=2):
    return dict(item_id=uid, http_start_s=start, elapsed_s=elapsed,
                completion_s=start+elapsed, admission_wait_s=.01,
                decisions=2, valid_decisions=2, correct_decisions=correct,
                complete_valid=True, status='success', http_status=200,
                response={'usage': {'input_tokens': 100}})


class AccountingTests(unittest.TestCase):
    def test_completion_window_and_admitted_cohort_are_distinct(self):
        cell=dict(warmup_s=1, window_s=2, model='jev-1.13.0')
        rows=[row(start=.8, elapsed=.4), row(start=1.5), row(start=2.9, elapsed=.5)]
        s=r.summarize(rows,cell,3.4,None,[],{'a':2})
        self.assertEqual(s['window_completed_requests'],2)
        self.assertEqual(s['cohort_requests'],2)
        self.assertEqual(s['valid_decisions_per_s'],2)
        self.assertAlmostEqual(s['cost']['usd_upper'],200*.042/1e6)
        self.assertTrue(s['full_window'])

    def test_accuracy_not_biased_by_packet_replay_frequency(self):
        rows=[row(correct=2) for _ in range(9)]+[row('b',correct=0)]
        s=r.summarize(rows,dict(warmup_s=1,window_s=2,model='jev-1.13.0'),3,None,[],{'a':2,'b':2})
        self.assertEqual(s['cohort_accuracy'],.9)
        self.assertEqual(s['balanced_accuracy'],.5)
        rows[0].pop('response')
        s=r.summarize(rows,dict(warmup_s=1,window_s=2,model='jev-1.13.0'),3,None,[],{'a':2,'b':2})
        self.assertIsNone(s['cost']['usd_per_1000_correct_upper'])

    def test_actual_concurrency_and_incomplete_window(self):
        rows=[row(start=.5,elapsed=2),row(start=2,elapsed=2)]
        s=r.summarize(rows,dict(warmup_s=1,window_s=2,model='jev-1.13.0'),4,'service_error_circuit',[],{'a':2})
        self.assertEqual(s['max_http_concurrency'],2)
        self.assertAlmostEqual(s['mean_http_concurrency'],1.25)
        self.assertFalse(s['full_window'])

    def test_matrix_combines_batch_and_concurrency(self):
        cells=r.plan(r.DEFAULT_FAMILIES)
        self.assertEqual(len(cells),56)
        self.assertTrue(all(c['target']>1 and c['concurrency']>1 for c in cells))
        self.assertEqual({c['concurrency'] for c in cells if c['family']!='routing_200'},{8,32,64})


class LoadTests(unittest.IsolatedAsyncioTestCase):
    async def test_workers_refill_beyond_single_wave(self):
        active=peak=0
        async def fake(session,item,model,origin,admission_wait,timeout):
            nonlocal active,peak
            start=asyncio.get_running_loop().time()-origin
            active+=1
            peak=max(peak,active)
            await asyncio.sleep(.01)
            active-=1
            return row(start=start,elapsed=asyncio.get_running_loop().time()-origin-start)
        cell=dict(warmup_s=.01,window_s=.10,model='jev-1.13.0',concurrency=3)
        with patch.object(r,'request',fake):
            rows,s,_=await r.run_cell(None,[{'id':'a','gold':{'q1':'x','q2':'y'}}],cell,r.Pacer(),{'a':100},1)
        self.assertGreater(len(rows),3*2)
        self.assertEqual(peak,3)
        self.assertTrue(s['full_window'])

    async def test_pacer_spaces_admissions_and_obeys_deadline(self):
        loop=asyncio.get_running_loop()
        p=r.Pacer(requests_per_s=100, tokens_per_s=1000)
        deadline=loop.time()+.3
        stamps=await asyncio.gather(*(p.acquire(30,deadline) for _ in range(3)))
        self.assertTrue(all(b-a>=.029 for a,b in zip(stamps,stamps[1:])))
        p.pause(1)
        self.assertIsNone(await p.acquire(1,loop.time()+.01))

    async def test_error_circuit_stops_refilling(self):
        async def fake(session,item,model,origin,admission_wait,timeout):
            await asyncio.sleep(.001)
            result=row(start=asyncio.get_running_loop().time()-origin)
            result.update(status='timeout',http_status=None,valid_decisions=0,correct_decisions=0,complete_valid=False)
            return result
        cell=dict(warmup_s=0,window_s=1,model='jev-1.13.0',concurrency=2)
        with patch.object(r,'request',fake):
            rows,s,_=await r.run_cell(None,[{'id':'a','gold':{'q1':'x','q2':'y'}}],cell,r.Pacer(),{'a':100},1)
        self.assertEqual(s['stop_reason'],'service_error_circuit')
        self.assertLessEqual(len(rows),21)
        self.assertFalse(s['full_window'])

class ReportTests(unittest.TestCase):
    def test_finding_compares_matching_repeat_when_peer_aborted(self):
        import render_throughput_docs as docs
        cost=dict(unpriced_requests=0,usd_per_1000_correct_lower=.01,usd_per_1000_correct_upper=.01)
        def repeat(index,rate):
            return dict(repeat=index,valid_per_s=rate,accuracy=.8,cost=cost)
        result={'modes':[
            dict(family='f',concurrency=32,model='jev-1.13.0',full_repeats=2,valid_per_s=999,accuracy=.8,cost=cost,repeat_metrics=[repeat(0,10),repeat(1,20)]),
            dict(family='f',concurrency=32,model='deepseek-flash',full_repeats=1,valid_per_s=15,accuracy=.8,cost=cost,repeat_metrics=[repeat(0,15)])]}
        text=docs.finding(result,'f')
        self.assertIn('仅第 1 轮',text)
        self.assertIn('10.0 个合法判断',text)
        self.assertNotIn('999',text)

    def test_recomputed_aggregate_uses_window_completions_and_balanced_accuracy(self):
        import build_sustained_throughput_report as report
        cell=dict(warmup_s=1,window_s=2,model='jev-1.13.0',family='f',concurrency=8,repeat=0)
        rows=[row('a',start=.5,elapsed=1),row('a'),row('b',start=2.5,elapsed=1,correct=0)]
        summary=r.summarize(rows,cell,3.5,None,[],{'a':2,'b':2})
        result=report.aggregate({}, {},[{'id':'a','family':'f','gold':{'q':0,'r':1}}, {'id':'b','family':'f','gold':{'q':0,'r':1}}],[(summary,rows)],[])
        m=result['modes'][0]
        self.assertEqual(m['valid_per_s'],2)
        self.assertEqual(m['accuracy'],.5)
        self.assertEqual(m['cohort_requests'],2)
        self.assertEqual(m['mean_http_concurrency'],summary['mean_http_concurrency'])
        self.assertIn('配置并发',report.task_section(result,'f'))

    def test_incomplete_stages_not_mixed_into_complete_window_results(self):
        import build_sustained_throughput_report as report
        cell=dict(family='f',model='jev-1.13.0',concurrency=8,repeat=0,skipped='service_error_circuit')
        result=report.aggregate({}, {},[],[(cell,[])],[])
        self.assertEqual(result['modes'][0]['full_repeats'],0)
        self.assertNotIn('valid_per_s',result['modes'][0])

class DnsTests(unittest.IsolatedAsyncioTestCase):
    async def test_resolver_reuses_system_answers_without_endpoint_override(self):
        answers=[dict(hostname='api.example.test',host='192.0.2.1',port=443,family=2,proto=6,flags=0)]
        resolver=r.RunResolver('api.example.test',answers)
        self.assertEqual(await resolver.resolve('api.example.test',443),answers)
        with self.assertRaises(OSError):
            await resolver.resolve('different.example.test',443)


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_http_total_timeout_and_no_retry(self):
        import socket
        from aiohttp import web
        calls=[]
        async def handler(request):
            calls.append(await request.json())
            if len(calls)==1:
                return web.Response(status=429,headers={'Retry-After':'1'},text='rate limited')
            await asyncio.sleep(.15)
            return web.json_response({})
        app=web.Application()
        app.router.add_post('/',handler)
        server=web.AppRunner(app)
        await server.setup()
        sock=socket.socket()
        sock.bind(('127.0.0.1',0))
        port=sock.getsockname()[1]
        site=web.SockSite(server,sock)
        await site.start()
        item={'id':'a','family':'f','request':{'state':{},'questions':{'q':{'criteria':{'yes':'Yes'}}}},'gold':{'q':'yes'}}
        config={**r.task.clinical.MODELS['deepseek-flash'],'endpoint':f'http://127.0.0.1:{port}/'}
        try:
            async with r.aiohttp.ClientSession() as session:
                with patch.dict(r.task.clinical.MODELS,{'deepseek-flash':config}):
                    origin=asyncio.get_running_loop().time()
                    limited=await r.request(session,item,'deepseek-flash',origin,0,1)
                    self.assertEqual(limited['http_status'],429)
                    self.assertEqual(limited['response_headers']['retry-after'],'1')
                    self.assertEqual(len(calls),1)
                    timed=await r.request(session,item,'deepseek-flash',origin,0,.03)
                    self.assertEqual(timed['status'],'timeout')
                    self.assertLess(timed['elapsed_s'],.12)
                    self.assertEqual(timed['correct_decisions'],0)
                    self.assertEqual(len(calls),2)
        finally:
            await server.cleanup()


@unittest.skipUnless((r.RUN / 'archive_manifest.json').exists(), 'Formal load still running')
class ArchiveTests(unittest.TestCase):
    def test_formal_archive_recomputes_from_raw_responses(self):
        import build_sustained_throughput_report as report
        result=report.aggregate(*report.verify(r.RUN))
        self.assertEqual(result['cells'],56)
        self.assertEqual(len(result['config']['families']),4)
        self.assertEqual(result['calibration_requests'],62)
        self.assertTrue(all(m['packet_sizes']==[8] for m in result['modes'] if m['family']!='routing_200' and m['full_repeats']))
        self.assertEqual(result['status']['fatal'],None)

    def test_tampered_score_rejected_after_archive_hash_updated(self):
        import tempfile,shutil,json
        import build_sustained_throughput_report as report
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'run'
            shutil.copytree(r.RUN,target)
            path=target/'cell-000.jsonl'
            rows=list(r.data.read_jsonl(path))
            rows[0]['correct_decisions']=rows[0]['decisions']+1
            r.data.write_jsonl(path,rows)
            manifest=json.loads((target/'archive_manifest.json').read_text())
            manifest['files']['cell-000.jsonl']=r.data.file_sha(path)
            r.data.write_json(target/'archive_manifest.json',manifest)
            with self.assertRaisesRegex(ValueError,'score mismatch'):
                report.verify(target)


if __name__=='__main__':
    unittest.main()
