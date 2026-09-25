"""Case counts must not inflate when fields or scan variants are repeated."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_case_inventory import case_key
class CaseIdentityTests(unittest.TestCase):
 def row(self,task,id_,group):return {'task':task,'id':id_,'group':group,'metadata':{}}
 def test_scan_variants_share_case_but_distinct_documents_do_not(self):
  a=self.row('clinocr_ocr_doctype','normal_t1_s2','template_1');b=self.row('clinocr_ocr_doctype','handwriting_t1_s2','template_1');c=self.row('clinocr_ocr_doctype','normal_t1_s3','template_1')
  self.assertEqual(case_key(a),case_key(b));self.assertNotEqual(case_key(a),case_key(c))
 def test_multiple_audio_fields_share_one_consultation(self):
  a=self.row('primock_asr_fields','c1:duration','c1');b=self.row('primock_asr_fields','c1:location','c1');c=self.row('primock_asr_fields','c2:duration','c2')
  self.assertEqual(case_key(a),case_key(b));self.assertNotEqual(case_key(a),case_key(c))
 def test_annotation_group_is_not_the_document_identity(self):
  a=self.row('nubes_scope_status','sectionA:T1','SAMPLE-001');b=self.row('nubes_scope_status','sectionA:T2','SAMPLE-001');c=self.row('nubes_scope_status','sectionB:T1','SAMPLE-001')
  self.assertEqual(case_key(a),case_key(b));self.assertNotEqual(case_key(a),case_key(c))
if __name__=='__main__':unittest.main()
