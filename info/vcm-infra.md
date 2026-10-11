# Infra for VCM

## Introduccion
- Las hipótesis son baratas de generar, la verificación contra verdad experimental con datos reales y no sinteticos es el cuello de botella. Por lo tanto, la arquitectura compleja, modelos de IA, no compensa la falta de cobertura de dato real
- Escalar el dato correcto es mucho más valioso que escalar parámetros de modelos
- Para tu investigación, Noetik es la referencia más útil que has traído hasta ahora para pensar el problema que probablemente más te interesa en última instancia: cómo llevar un VCM del nivel de célula aislada al nivel de tejido/sistema, que es literalmente tu objetivo declarado al inicio de este proyecto. Ninguno de los otros actores (Arc, Tahoe, scGPT, GEARS) resuelve eso nativamente — todos operan sobre suspensiones de célula única sin arquitectura espacial. El coste de esa ventaja es que, a diferencia de Tahoe-100M o Arc Virtual Cell Atlas, no vas a poder acceder a los datos ni pesos de Noetik — es 100% cerrado.
- No es que el contexto espacial haga "mejores" los modelos de forma universal, es que desbloquea un tipo de información que es estructuralmente invisible para cualquier modelo entrenado en célula disociada, y eso tiene un valor añadido concreto y demostrable, pero también límites que conviene que tengas claros.

## Modelos
- Tahoe-x1 - Tahoe Therapeutics - Oncologia
- ST-Tahoe - Arc Institute - Oncologia and Biologia General
    Modelo con licencia de uso gratis pero no comercial
    Puede ser mas eficiente que Tahoe-x1
    STATE/ST-Tahoe está diseñado y optimizado exactamente para eso y sus benchmarks reportados son más fuertes en esa tarea concreta — pero te ata a una licencia que, si algún día quieres colaborar con industria o llevar algo a producto, te obliga a negociar. Tahoe-x1 es más generalista (mejor como encoder de propósito amplio) y te da libertad legal total, a costa de no estar tan afinado específicamente para la tarea de transición-por-perturbación como STATE.

- Rhaister - Tahoe Therapeutics:
    Un modelo estadístico elegante construido directamente sobre estadísticas resumen de los datos, en vez de arquitecturas complejas tipo virtual cell model — y reportan que con solo un puñado de perturbaciones de ejemplo en un contexto nuevo, predice respuestas para otras perturbaciones con precisión dentro del ruido experimental, superando a los virtual cell models de última generación en rendimiento, siendo el primer modelo que muestra escalado consistente con más datos de perturbación. Su propia conclusión: escalar el dato correcto es mucho más valioso que escalar parámetros — el mismo mensaje de GEARS vs. scGPT/Geneformer, viniendo ahora de la propia empresa que construye los datasets más grandes del campo

- ScGPT - University of Toronto - Biologia General
- Geneformer - NVIDIA, part of BioNemo - Biologia General
    SCgpt y Geneformer se entrenan autospuervisado, con datos sin pertubar
    Nunca vieron el par causa-efecto
    GEARS tiene mejor performance porque tiene datos de perturbacion (causa-efecto o datos intervencionales, no observacionales)

- GEARS - Standford - GNN - Biologia General:
    Predecir el resultado de perturbaciones multigénicas nunca vistas.
    Mejor que scGPT + Geneformer - ya que esta entrenado en datos validados.
    La pieza clave es que el uso de los grafos de relación génica y de perturbación permite a GEARS generalizar a genes que nunca fueron perturbados experimentalmente durante el entrenamiento. Porque aunque no haya visto ese gen concreto perturbado, sí conoce su posición en la red de relaciones biológicas (co-expresión, anotaciones funcionales GO) y puede inferir por analogía estructural

- TARIO 2 - Noetik - Oncology:
    Entrenado sobre miles de muestras de cáncer humano a través de 19 tipos de cáncer, aprendiendo la relación entre imágenes de patología pretratamiento estándar (H&E) y datos de transcriptómica espacial de alta resolución
    No mide transcriptómica espacial directamente en el momento de uso — la infiere a partir de la imagen H&E, apoyándose en lo aprendido durante el entrenamiento sobre pares H&E↔spatial-seq reales. Es un proxy predicho, no una medición — así que hereda el mismo riesgo epistémico que discutimos con los datos sintéticos: es tan bueno como la fidelidad de esa relación aprendida, y probablemente se degrada en tejidos o contextos moleculares infrarrepresentados en su set de entrenamiento de 19 tipos de cáncer. 


## Datasets
- Arc Virtual Cell Atlas:
    Suma más de 300 millones de células accesibles gratuitamente desde el 25 de febrero de 2025, combinando Tahoe-100M (Tahoe Therapeutics) y scBaseCount (200M células de 21 especies, curadas y reprocesadas con agentes de IA a partir de repositorios públicos por el propio Arc) — ambos componentes son de acceso abierto, sin gate de licencia comercial.
    Es decir: los datos de Arc son libres; son los modelos entrenados sobre ellos (State/SE-600M/ST-Tahoe) los que llevan la licencia restrictiva — separa bien esa distinción dataset vs. modelo en tu documentación de proyecto, porque tiene implicaciones legales distintas.

## Iniciativas
- Arc Institute - VCI - Virtual Cell Initiative:
    Construir un modelo de ML preciso que prediga cómo distintos tipos y estados celulares responden a drogas y perturbaciones genéticas, para identificar qué "palancas" mover para llevar una célula de un estado enfermo a uno sano.
    No vende nada; su output son papers, modelos y datasets abiertos, financiados por donación filantrópica.
- Tahoe Therapeutics:
    Junio 2026 han declarado un giro estratégico interesante: en vez de perseguir solo un modelo unificado y generalista de la célula, están apostando por generar datos de alta calidad y precisión a una escala más allá de lo que el campo persigue hoy, para luego sumergir modelos de razonamiento en esas mediciones ya hechas — es decir, usar reasoning models (tipo LLM agéntico) apoyados en una base de "verdad experimental" masiva, en vez de depender únicamente de un solo foundation model monolítico entrenado end-to-end.
- Noetik:
    Construye su plataforma sobre datos espaciales multimodales de tejido tumoral humano real, no solo transcriptómica de célula disociada.
    Combinan omics espacial (proteómica + transcriptómica in situ, preservando la arquitectura del tejido) con una plataforma propia de perturbación in vivo llamada Perturb-Map
    Su modelo, OCTO-VC (parte de la plataforma más amplia OCTO, "Oncology Counterfactual Therapeutics Oracle"), es un modelo de célula única transcriptómico espacial entrenado con aprendizaje auto-supervisado para simular la expresión génica de célula única espacialmente resuelta en tejidos de paciente intactos o "virtuales", usando prompts y contexto de vecindario local para predecir patrones de expresión génica. El framing "counterfactual" es literal: están vendiendo la capacidad de preguntar "¿qué pasaría si...?" sobre biología de paciente real, yendo más allá de los datos limitados disponibles de cualquier paciente individual, para simular resultados de terapéuticas antes de que entren en clínica.
    Noetik sube un peldaño en la escalera célula→tejido→cuerpo, no la escalera completa.
    Pero ni Noetik ni ningún VCM actual capturan el knob de cuerpo: no hay flujo sanguíneo, tráfico inmune sistémico, ni farmacocinética real en una sección de tejido fijada en un portaobjetos — eso sigue siendo tan inalcanzable para spatial transcriptomics como lo es para un organoide sin vascularización

## Conclusiones
- El valor añadido de Noetik es real y específico — resuelve el problema de vecindad/microambiente que ningún modelo de célula disociada puede resolver por diseño, y lo hace con una aplicación práctica inteligente **(inferir desde H&E barato en vez de requerir spatial-seq caro)**. Pero no es "un modelo mejor" en términos absolutos frente a Tahoe-x1/scGPT — resuelve una pregunta biológica distinta (interacción celular en contexto tisular) que complementa, no reemplaza, la pregunta que resuelven los modelos de perturbación a nivel de célula individual que ya tienes en tu radar. Para tu propio pipeline de VCM oncológico, esto sugiere que la arquitectura ideal probablemente combine ambas capas — perturbación a nivel de célula individual (Tahoe-x1/GEARS) y contexto espacial de vecindario (inspirado en el enfoque de OCTO-VC) — en vez de escoger una sobre otra.
- Hay un límite superior a lo que se puede aprender de un dataset dado — todos los trucos de entrenamiento y mejoras de modelo del mundo no pueden sortear el hecho de que solo hay tanto que se puede extraer de un dataset concreto, y concluye que el próximo cambio de paradigma no vendrá de una mejora al RL o un tipo nuevo de red neuronal, vendrá **cuando desbloqueemos una fuente de datos a la que no hemos accedido antes, o que no hemos aprovechado adecuadamente todavía**.
- El problema no es solo procesar más datos, es que la **caracterización molecular de la mayoría de tumores todavía no está ligada a los desenlaces clínicos reales de tratamiento** — que es exactamente el hueco que Noetik/TARIO-2 y Tahoe intentan llenar cada uno a su manera.
- La pregunta más valiosa que puedes hacerte al diseñar tu pipeline no es "qué modelo uso" sino "qué tipo de dato nuevo, no capturado todavía por Tahoe-100M/scGPT/HCA, podría desbloquear la pregunta específica que quiero responder"
- Para pronóstico/diagnóstico y predicción de evolución del tumor, **el hueco no es volumen, es longitudinalidad**. TCGA, GDC, CPTAC son mayormente snapshots transversales (una biopsia, un momento). Para modelar evolución necesitas **series temporales del mismo paciente: biopsias líquidas seriadas (ctDNA), muestreo repetido pre/post tratamiento, seguimiento clínico prolongado ligado a esas muestras moleculares**. Esto es caro y logísticamente difícil (requiere consentimiento longitudinal, infraestructura clínica sostenida), pero es la pieza que ningún atlas actual resuelve bien — es la "nueva modalidad" que Morris diría que falta desbloquear en oncología.
- Interventional data (perturbation ground truth) is the true bottleneck in VCM development, not observational genomic data.
Observational vs. interventional datasets: **TCGA-style data captures tumor state; datasets like Tahoe-100M and DepMap capture cause-effect perturbation relationships — the true bottleneck for VCMs.**
- **El problema de gobernanza/interoperabilidad de datos clínicos reales, probablemente el cuello de botella menos técnico y más institucional/regulatorio de todos, y el que menos atención mediática recibe frente a "más GPUs, más parámetros"**.


## Objetivo
- Tener un modelo, independientemente de la arquitectura, (VCM celular disociado, o VCM spatial con el contexto del tejido vecinal, GPT, Bert, Transfomer, GNN, CNN), para que el modelo pueda inferir que tratamiento/medicacion sera mejor para un caso de un paciente oncologico, teniendo datos de una muestra de una biopsia: (omicos, spatial, H&E). Poder inferir que medicacion va a funcionar. Incluso diseñar la molecular que va a funcionar (proteina, conjugado con anticuerpo, vacuna ARNm).
- Quiza lo que se busca aqui son diseñar vacunas (pueden ser ARNm), o proteinas (con AlphaFold) contra el cancer de una forma personalizada. Muy especificas contra el tumor, sabiendo los datos omicos, spatial y H&E del tumor. 
- Ya que la poblacion celular de un tumor puede ser muy diversa geneticamente, podria hasta ser necesario una molecula/proteina/vacuna ARNm por cada subpoblacion celular de cada tumor del paciente. Entonces necesitamos perfilar con datos omicos cada sub-tumor. Pero la idea es conseguir esa molecula/proteina/vacuna ARNm para cada sub-tumor sabiendo su perfil omico y teniendo el modelo o conjunto de modelos que interpreten esos datos omicos. 
- Para poder entrenar y construir este tipo de modelos que te de una receta personalizada para cada caso especifico, teniendo los datos del perfil de tumor, quiza para los datos se necesite un pipeline de interoperabilidad entre la recoleccion fisica y digital. Ya que me dijiste que el cuello de botella o problema esta en obtener esos datos clinicos reales en forma de series temporales del mismo paciente: biopsias líquidas seriadas (ctDNA), muestreo repetido pre/post tratamiento, seguimiento clínico prolongado ligado a esas muestras moleculares, con anotaciones medicas del oncologo especialista. 
- el problema de transferencia línea celular → paciente real: cómo adaptar/validar un modelo entrenado in vitro para que generalice a muestras de paciente - Se trata de cerrar el gap in-vitro-in-vivo


## Resumen Objetivo
1. Perfilar
2. Predecir
3. Diseñar
4. Validar

Etapa A — Perfilado y estratificación del tumor. 
Partir de la muestra (ómica + spatial + H&E) y caracterizar la heterogeneidad intratumoral: identificar las subpoblaciones clonales genéticamente distintas. Aquí es donde entran los modelos que ya mapeamos (Tahoe-x1, scGPT para representación; TARIO-2/OCTO como referencia para la capa espacial). Esta etapa es la más madura — es esencialmente un problema de embedding + clustering + deconvolución, y hay herramientas establecidas.

Etapa B — Predicción de respuesta a tratamiento. 
Dado el perfil de cada subpoblación, inferir qué terapia existente funcionaría mejor. Esto es predicción de perturbación aplicada a fármacos reales — el terreno de GEARS, STATE, Rhaister. El límite conocido que ya discutimos: estos modelos predicen bien dentro del espacio de perturbaciones que vieron (líneas celulares, fármacos del cribado), y su generalización a un paciente real concreto está mucho menos validada.

Etapa C — Diseño de novo de la terapia. 
Aquí das un salto a otra disciplina entera. Diseñar una proteína, un ADC o una vacuna de ARNm no es predicción de perturbación — es diseño molecular generativo, y usa modelos completamente distintos:

Proteínas/binders → AlphaFold3, RFdiffusion, ProteinMPNN (familia Baker Lab), ESM.
Neoantígenos para vacunas ARNm → predicción de neoantígenos (netMHCpan y sucesores), predicción de presentación MHC, y el reto real que es predecir inmunogenicidad, no solo binding.
ADCs → selección de diana de superficie + química de conjugación (el terreno del JV Tahoe-Alloy que vimos).

Etapa D — La infraestructura de datos longitudinales que los sostiene a todos 
El cuello de botella clínico-institucional que ya identificamos.


Lo que no está resuelto, y donde está tu oportunidad real, es exactamente la parte de transferencia a paciente: los modelos que rinden 0.8+ de correlación en líneas celulares se desploman al aplicarse a datos de paciente real (TCGA con desenlace de tratamiento, o cohortes clínicas). Así que tu diferenciador no es "otro predictor sobre GDSC", sino "cómo cierro el gap in vitro → in vivo" — mantén ese norte, porque es fácil deslizarse hacia el problema fácil y ya resuelto sin darse cuenta.

El ecosistema oncología+IA se organiza en capas de una cadena de valor, y ahora las tienes casi todas mapeadas:

1. Generación de datos moleculares a escala → Tahoe, Arc, Noetik, Resolute
2. Datos clínicos reales + diagnóstico → Tempus (y sus vecinos Guardant, Foundation Medicine, Flatiron)
3. Modelos fundacionales / predicción → tu terreno (Tahoe-x1, scGPT, STATE, GEARS)
4. Diseño de terapia → FinalDose (y BioNTech/Moderna en vacunas ARNm)
5. Aplicación clínica → BIOS Life

**El problema es el acceso a Datos no el construir modelos.** 
