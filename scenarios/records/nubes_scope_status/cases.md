# 西班牙文否定与不确定性：逐案例结果

79 个案例，共 100 条测试记录。案例口径：不同源文件临床片段（同一片段多个标注合并）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| sample-006.intme.chico | {"excerpt": "ódice por hipoglucemia .\nDolor en paciente con isquemia arterial crónica extremidades .\nTTo ahb… | 1 | 100.0% | 100.0% |
| sample-008.urolo.preil | {"excerpt": "eriormente ingresa en retención urinaria , colocando sonda vesical , se aconseja IQ de prostata .… | 1 | 100.0% | 100.0% |
| sample-008.cardi.progr | {"excerpt": "as externas de cardiologia .\nEl cuadro clinico mejora claramente con protección gastrica .\nEl E… | 1 | 100.0% | 100.0% |
| sample-003.shosu.progr | {"excerpt": "bién rehabilitación de la marcha en llano y subir/bajar escaleras .\nEvoluciona a exitus .\nPrese… | 2 | 100.0% | 100.0% |
| sample-004.sugen.chico | {"excerpt": "l , episodios de vómitos en la ultima semana .\nTratada y curada por su MAP/DUE , desde entonces … | 1 | 0.0% | 0.0% |
| sample-005.shosu.progr | {"excerpt": "rado la autonomia de la marcha .\nEl paciente presenta los siguientes problemas : - Se detecta fi… | 2 | 50.0% | 100.0% |
| sample-004.neuro.progr | {"excerpt": "recto de anticoagulación y la ausencia de datos sugestivos de proceso isquémico agudo en las prue… | 6 | 50.0% | 66.7% |
| sample-004.shosu.progr | {"excerpt": "sta a tratamiento con hierro oral .\nEn los dias posteriores control de la sintomatologia con la … | 1 | 0.0% | 0.0% |
| sample-003.intme.chico | {"excerpt": ".\nVarón de 71 años pluripatológico , EPOC severo , cardiópata , FA , dado de alta en este Centro… | 1 | 100.0% | 100.0% |
| sample-008.intme.progr | {"excerpt": "estudio cardiológico arriba indicado apreciándose en el estudio holter ECG bradicardia sin que ha… | 1 | 0.0% | 100.0% |
| sample-009.homho.preil | {"excerpt": "de se ajustó el tratamiento aumentando la dosis y variando la hora de administración , con lo cua… | 2 | 100.0% | 100.0% |
| sample-001.ginec.diate | {"excerpt": "UROLOGIA - Interconsulta en Hospitalización Pequeña carúncula uretral .\nHígado , bazo , páncreas… | 2 | 100.0% | 100.0% |
| sample-005.homho.progr | {"excerpt": " herida quirúrgica y cambiamos tratamiento a Ciprofloxacino .\nNiega dolor , en la cama se encuen… | 3 | 100.0% | 66.7% |
| sample-010.cardi.preil | {"excerpt": "emanas en contexto de insuficiencia cardiaca .\nAnte ese conjunto de sintomas ingresa .\nNo clíni… | 1 | 100.0% | 100.0% |
| sample-003.otorh.progr | {"excerpt": "ajo anestesia general .\nAmigdalitis pultacea .\nSe retira con fecha 4/17/12 , no sangra .\nAmigd… | 2 | 100.0% | 100.0% |
| sample-006.shosu.preil | {"excerpt": " el 19/11/2014 presentando fractura C2 .\nFractura - luxación bimaelolar tobillo derecho tras cai… | 1 | 100.0% | 100.0% |
| sample-004.shosu.phyex | {"excerpt": "arálisis facial derecha de origen central .\nA nivel de extremidades presenta paresia completa de… | 1 | 100.0% | 100.0% |
| sample-008.shosu.progr | {"excerpt": "n pélvica y dismetria de MMII asociada ) .\nLa paciente es informada de enfermedad incurable y qu… | 1 | 100.0% | 100.0% |
| sample-010.traum.preil | {"excerpt": "ante izdo .\nPresenta déficit motor con parálisis CPE desde hace unos 7 años ( según el paciente … | 1 | 100.0% | 100.0% |
| sample-008.traum.chico | {"excerpt": "mido cada 8h ) y al reevaluarlo hoy , derivan .\nDolor en nalga dcha desde hace 6 días , en tto c… | 1 | 0.0% | 100.0% |
| sample-008.homho.phyex | {"excerpt": "ilina , ceftriaxona , tetraciclina , clindamicina , vancomicina , levofloxacino y moxifloxacino .… | 1 | 100.0% | 100.0% |
| sample-001.intcu.progr | {"excerpt": ".\nCon fecha de 26/11 asocia al tratamiento antibiotico de amplio espectro con piperazilina-tazob… | 1 | 100.0% | 100.0% |
| sample-008.traum.phyex | {"excerpt": "icit sensitivomotor .\nDolor en interlínea medial de rodilla dcha , no dolor en interlínea latera… | 1 | 100.0% | 100.0% |
| sample-008.traum.diate | {"excerpt": "nterconsulta NEUROLOGÍA ID : probable plexopatia/radiculopatia L5-S1 por tracción/compresion por … | 1 | 0.0% | 100.0% |
| sample-002.sugen.progr | {"excerpt": "on necesidad de perfusión de noradrenalina a altas dosis .\nActualmente la paciente está afebril … | 2 | 100.0% | 100.0% |
| sample-005.shosu.diate | {"excerpt": "Bazo no visualizado .\nMínimo temblor de actitud bilateral .\nA valorar posibilidad clínica de co… | 2 | 50.0% | 50.0% |
| sample-010.sugen.progr | {"excerpt": "ara control posterior en Consultas Externas .\nPaciente diagnosticada de apendicitis aguda compli… | 1 | 100.0% | 100.0% |
| sample-010.intme.progr | {"excerpt": " existencia de spseudomona y enterococo sensible a tazocel en la orina por lo que se inició trata… | 1 | 100.0% | 100.0% |
| sample-001.neuro.progr | {"excerpt": "79 años con antecedentes de cardiopatia isquémica : Triple pontaje aorto coronario ( hace 20 años… | 1 | 100.0% | 100.0% |
| sample-001.intcu.preil | {"excerpt": "tratandola como paciente EPOC .\nTA en todo momento en torno a 90-110 de TAs . mantiene diuresis … | 1 | 100.0% | 100.0% |
| sample-002.homho.diate | {"excerpt": "matosclerosis\nDesignado citologia por impronta de material de lesión en muslo derecho : - CITOLO… | 1 | 100.0% | 100.0% |
| sample-007.homho.recom | {"excerpt": "de Atención Primaria quien realizará las modificaciones que considere oportunos en el tratamiento… | 1 | 100.0% | 100.0% |
| sample-004.traum.diate | {"excerpt": "nistración de CIV se observa importante captación del mismo por parte de las estructuras óseas af… | 1 | 100.0% | 100.0% |
| sample-003.cardi.chico | {"excerpt": " se han ido acentuandose e intensificansose , con irradiación hacia la escotadura yugular .\nPaci… | 1 | 100.0% | 100.0% |
| sample-010.cardi.progr | {"excerpt": "a la izquierda y formas inmaduras mas un gran aumento de los valores de BNP .\nEn urgencias al in… | 2 | 100.0% | 100.0% |
| sample-007.homho.preil | {"excerpt": "stro servicio para confirmar llegada de analitica y comentar la evolución .\nNo otra clínica acom… | 1 | 100.0% | 100.0% |
| sample-001.otorh.chico | {"excerpt": "siendo tratada con aine 's .\nNo perdida de fuerza ni de sensibilidad en extremdiades .\nEn las i… | 1 | 100.0% | 100.0% |
| sample-002.shosu.progr | {"excerpt": "encia a la hipopotasemia .\nDesde el punto de vista rehabilitador la paciente se muestra colabora… | 1 | 100.0% | 100.0% |
| sample-007.traum.chico | {"excerpt": "No pérdida de conciencia ni focalidad .\nDolor en mano izq y erosiones .\nCaida de la moto a las … | 1 | 100.0% | 100.0% |
| sample-007.homho.phyex | {"excerpt": "Colesterol : 86 .\nAscitis y carcinomatosis peritoneal .\nEngrosamiento IM ; pequeña placa calcif… | 1 | 100.0% | 100.0% |
| sample-009.neuro.progr | {"excerpt": "orma ambulatoria según se indica más abajo .\nSe le han practicado las exploraciones complementar… | 2 | 100.0% | 100.0% |
| sample-004.shosu.preil | {"excerpt": " Stryker ® ) encerrojado distalmente .\nIngreso en la Unidad para rehabilitacion de la marcha y c… | 1 | 0.0% | 100.0% |
| sample-010.homho.preil | {"excerpt": "erida por lo que se le pautó por su M. de Familia Augmentine cambiandolo a los 3 días a Cefditore… | 2 | 0.0% | 50.0% |
| sample-009.homho.phyex | {"excerpt": "e inicia tratamiento con cefotaxima a dosis altas y dexametasona .\nVena porta normal .\nSe nos c… | 1 | 100.0% | 100.0% |
| sample-002.neuro.progr | {"excerpt": " origen neurálgico y la ausencia de mejoría con el tratamiento con FAEs , asi como la presencia d… | 4 | 25.0% | 25.0% |
| sample-007.neuro.preil | {"excerpt": "uego holocraneal con predominio frontemporal .\nEncontrándose previamente bien ingresa por presen… | 1 | 0.0% | 0.0% |
| sample-009.shosu.preil | {"excerpt": "en cardioembólico el 20/04/12 con evolucion favorable presentando al alta de agudos una puntuacio… | 1 | 100.0% | 100.0% |
| sample-010.sugen.preil | {"excerpt": " .\nPaciente intervenido en 2.005 por Neoplasia de recto con amputación abdominoperineal .\nTrata… | 1 | 100.0% | 100.0% |
| sample-003.neuro.progr | {"excerpt": "ca de sangre de control en el que se apreció disminución de la PCReactiva y se constató la presen… | 1 | 100.0% | 0.0% |
| sample-004.sugen.progr | {"excerpt": "asintomático , persistiendo discreta elevación de transaminasas hepáticas .\nDurante su ingreso h… | 1 | 0.0% | 0.0% |
| sample-004.homho.progr | {"excerpt": "to ya ha sido dado de alta por el Servicio de Rehabilitación .Durante este proceso , sufre dos ep… | 1 | 0.0% | 0.0% |
| sample-010.homho.chico | {"excerpt": " Gomez ) .\nVarón de 74 años de edad que es derivado a nuestro Servicio desde el Servicio de Medi… | 1 | 100.0% | 100.0% |
| sample-001.sugen.diate | {"excerpt": "teoporosis , llama la atención una pequeña pérdida de altura de ambos platillos D11 , sobre todo … | 1 | 100.0% | 100.0% |
| sample-004.traum.preil | {"excerpt": " asintomática .\nNo tumefacción , no bloqueos , Dolor en la cama según postura .\nIntervenida con… | 1 | 0.0% | 0.0% |
| sample-006.neuro.progr | {"excerpt": " y por lo que hemos optado por la introduccion de nebivolol y la suspension de enalapril .\nExitu… | 1 | 0.0% | 0.0% |
| sample-009.intme.progr | {"excerpt": "informe remitimos al paciente a Endocrinologo de área para valorar la situación y otras opciones … | 1 | 100.0% | 100.0% |
| sample-004.intme.progr | {"excerpt": "tensa .\n- Anemia multifactorial que fué transfundida .\n- Anemia mixta por perdida digestiva y d… | 1 | 100.0% | 100.0% |
| sample-008.cardi.preil | {"excerpt": "vómitos que imiden ingesta oral , y por la noche sobre las 21pm comienza con dolor en hombro izqu… | 1 | 0.0% | 0.0% |
| sample-007.cardi.preil | {"excerpt": "pm , QRS normal , no alteraciones en la repolarización , lo deriva para valoración .\nNo aparente… | 1 | 0.0% | 0.0% |
| sample-006.traum.preil | {"excerpt": "odilla izda implantada en sept-2016 , con buena evolución postoperatoria y el paciente deambuland… | 1 | 100.0% | 100.0% |
| sample-008.neuro.preil | {"excerpt": "s de Urgencia que fueron a atenderle a su domicilio , el paciente fue encontrado en estado estupo… | 1 | 100.0% | 100.0% |
| sample-005.homho.recom | {"excerpt": "as 11,46 horas - Seguimiento por su médico de Atención Primaria\n.Pantoprazol 40mg , 1comp en la … | 1 | 100.0% | 100.0% |
| sample-007.shosu.chico | {"excerpt": "aresia derecha .\nPaciente de 86 años de edad que ingresa para rehabilitación de fractura de cade… | 1 | 100.0% | 100.0% |
| sample-010.sugen.chico | {"excerpt": "h .\nNo otra sintomatología añadida .\nEn tto con Claritromicina + Amoxicilina + Omeprazol , desd… | 1 | 100.0% | 100.0% |
| sample-005.shosu.chico | {"excerpt": "dos de Traumatologia - Instituto Florence Nightingale .\nPaciente que ingresa procedente de la un… | 1 | 100.0% | 100.0% |
| sample-009.homho.progr | {"excerpt": "s estable pudiendo incorporarse de la cama y deambular por su domicilio .\nDurante los cuatro pul… | 2 | 0.0% | 0.0% |
| sample-003.shosu.preil | {"excerpt": "aje con infección urinaria por e.coli Blee ( nosocomial ) .\nPaciente que acude desde la unidad d… | 1 | 100.0% | 100.0% |
| sample-007.sugen.diate | {"excerpt": " IC .\nAnalitica : leucocitosis 28.000 .\nValorar presencia de liquidos libre abdominal .\nLa pac… | 1 | 100.0% | 100.0% |
| sample-006.sugen.chico | {"excerpt": "En estudio en Centro de Salud Hagnódice por tumoracion que se aprecia en Mamografia de screning (… | 1 | 100.0% | 100.0% |
| sample-007.intme.progr | {"excerpt": "sovagal .\nPaciente pluripatológica y con deterioro cognitivo moderado , barthel basal menor de 5… | 1 | 100.0% | 100.0% |
| sample-003.sugen.preil | {"excerpt": "ue algo más estreñido .\nNo fiebre ni otra sintomatologia asociada .\nLa paciente no mejora con n… | 1 | 100.0% | 100.0% |
| sample-004.cardi.preil | {"excerpt": "alsartan .\nAntecedentes de estenosis aortica .\nHoy no taquicardia .\nAcude de nuevo por persist… | 1 | 100.0% | 100.0% |
| sample-008.homho.preil | {"excerpt": "a ósea que fué normal .\nPaciente diagnosticado en Diciembre de 2014 en Hospital de Alta Resoluci… | 1 | 100.0% | 100.0% |
| sample-007.sugen.chico | {"excerpt": "il. no dolor irradiado a otra localizacion .\nEsta mañana le han cambiado pañal normal. más tarde… | 1 | 0.0% | 0.0% |
| sample-006.supla.preil | {"excerpt": "de 3 x 4 cm\nRecidiva entropion ojo izquierdo\nPaciente que es atrapado MSD con una desbrozadora … | 1 | 100.0% | 100.0% |
| sample-010.traum.phyex | {"excerpt": "en , Aquileos disminuidos bilateral .\nRx Cadera D : signos artrosicos con osteofitosis\nDiscreta… | 1 | 0.0% | 0.0% |
| sample-003.intme.progr | {"excerpt": "ardiologia y Neurologia .\nSe inició tratamiento con levofloxacino y ante la mala evolución ingre… | 1 | 0.0% | 100.0% |
| sample-007.cardi.progr | {"excerpt": "lio con controles por consultas externas de cardiologia con el Dr. Reyes .\nCARDIOLOGIA : Pacient… | 1 | 100.0% | 0.0% |
| sample-002.cardi.preil | {"excerpt": "stá con Propafenona .\nNo mareo , no claro cortejo acompañante .\nHa tomado el vernies para el do… | 1 | 100.0% | 100.0% |
