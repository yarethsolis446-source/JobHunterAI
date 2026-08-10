import 'dart:io';
import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';

import '../models/job.dart';
import '../services/api_service.dart';
import '../widgets/job_card.dart';
import 'history_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() {
    return _HomePageState();
  }
}

class _HomePageState extends State<HomePage> {
  // =====================================================
  // EMPLEOS
  // =====================================================

  List<Job> empleos = [];

  // =====================================================
  // ESTADOS
  // =====================================================

  bool cargando = false;

  bool analizandoCV = false;

  bool generandoReporte = false;

  // =====================================================
  // PERFIL
  // =====================================================

  Map<String, dynamic>? perfil;

  // =====================================================
  // CV
  // =====================================================

  Uint8List? cvBytes;

  String? cvNombre;

  // =====================================================
  // FILTROS
  // =====================================================

  String? paisSeleccionado;

  bool soloRemoto = false;

  // =====================================================
  // PAISES
  // =====================================================

  final Map<String, String> paises = {
    'Costa Rica': 'cr',
    'Estados Unidos': 'us',
    'Canadá': 'ca',
    'México': 'mx',
    'España': 'es',
    'Reino Unido': 'gb',
    'Alemania': 'de',
    'Francia': 'fr',
    'Italia': 'it',
    'Portugal': 'pt',
    'Australia': 'au',
    'Brasil': 'br',
    'Argentina': 'ar',
    'Chile': 'cl',
    'Colombia': 'co',
    'Panamá': 'pa',
  };

  // =====================================================
  // BUSCAR EMPLEOS
  // =====================================================

  Future<void> cargarEmpleos() async {
    setState(() {
      cargando = true;
    });

    try {
      final datos = await ApiService.obtenerEmpleos(
        'software developer',
        pais: paisSeleccionado,
        remoto: soloRemoto,
      );

      if (!mounted) {
        return;
      }

      final resultados = datos
          .map<Job>((json) => Job.fromJson(Map<String, dynamic>.from(json)))
          .toList();

      setState(() {
        empleos = resultados;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('${resultados.length} empleos encontrados.')),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error obteniendo empleos: $e')));
      }
    } finally {
      if (mounted) {
        setState(() {
          cargando = false;
        });
      }
    }
  }

  // =====================================================
  // SELECCIONAR CV
  // =====================================================

  Future<void> seleccionarCV() async {
    try {
      final resultado = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf'],
        withData: true,
      );

      if (resultado == null) {
        return;
      }

      final archivo = resultado.files.single;

      final Uint8List? bytes = archivo.bytes;

      if (bytes == null) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('No se pudo leer el PDF.')),
          );
        }

        return;
      }

      cvBytes = bytes;

      cvNombre = archivo.name;

      if (mounted) {
        setState(() {
          analizandoCV = true;
        });
      }

      // =================================================
      // ENVIAR CV
      // =================================================

      final respuesta = await ApiService.analizarCV(
        archivo.name,
        bytes,
        pais: paisSeleccionado,
        remoto: soloRemoto,
      );

      if (!mounted) {
        return;
      }

      // =================================================
      // PERFIL
      // =================================================

      final perfilJson = respuesta['perfil'];

      Map<String, dynamic>? nuevoPerfil;

      if (perfilJson is Map) {
        nuevoPerfil = Map<String, dynamic>.from(perfilJson);
      }

      // =================================================
      // EMPLEOS
      // =================================================

      final empleosJson = respuesta['empleos'];

      List<Job> resultados = [];

      if (empleosJson is List) {
        resultados = empleosJson
            .map<Job>((json) => Job.fromJson(Map<String, dynamic>.from(json)))
            .toList();
      }

      // =================================================
      // ACTUALIZAR
      // =================================================

      setState(() {
        perfil = nuevoPerfil;
        empleos = resultados;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'CV analizado correctamente. '
            '${resultados.length} empleos encontrados.',
          ),
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error analizando CV: $e')));
      }
    } finally {
      if (mounted) {
        setState(() {
          analizandoCV = false;
        });
      }
    }
  }

  // =====================================================
  // LIMPIAR PANTALLA
  // =====================================================

  void limpiarPantalla() {
    setState(() {
      empleos = [];

      perfil = null;

      cvBytes = null;

      cvNombre = null;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text(
          'Pantalla limpiada. '
          'El historial no fue modificado.',
        ),
      ),
    );
  }

  // =====================================================
  // ABRIR HISTORIAL
  // =====================================================

  void abrirHistorial() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const HistoryPage()),
    );
  }

  // =====================================================
  // GENERAR REPORTE
  // =====================================================

  Future<void> generarReportePDF() async {
    if (cvBytes == null || cvNombre == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Primero debes seleccionar y analizar un CV.'),
        ),
      );

      return;
    }

    setState(() {
      generandoReporte = true;
    });

    try {
      final Uint8List pdfBytes = await ApiService.generarReportePDF(
        cvNombre!,
        cvBytes!,
      );

      final directorio = await getTemporaryDirectory();

      final ruta = '${directorio.path}/JobHunter_AI_Reporte.pdf';

      final archivoPDF = File(ruta);

      await archivoPDF.writeAsBytes(pdfBytes, flush: true);

      if (!await archivoPDF.exists()) {
        throw Exception('No se pudo guardar el reporte PDF.');
      }

      final resultado = await OpenFilex.open(ruta, type: 'application/pdf');

      if (!mounted) {
        return;
      }

      if (resultado.type != ResultType.done) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'PDF generado, pero no se pudo abrir.\n'
              'Código: ${resultado.type}',
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Reporte PDF generado correctamente.')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error generando el reporte PDF: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          generandoReporte = false;
        });
      }
    }
  }

  // =====================================================
  // PERFIL
  // =====================================================

  Widget construirPerfil() {
    if (perfil == null) {
      return const SizedBox.shrink();
    }

    final habilidades = perfil!['habilidades'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Perfil detectado',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 10),

            Text(
              'Profesión: '
              '${perfil!['profesion'] ?? 'No especificada'}',
            ),

            Text(
              'Nivel: '
              '${perfil!['nivel'] ?? 'No especificado'}',
            ),

            Text(
              'Experiencia: '
              '${perfil!['experiencia'] ?? 0} años',
            ),

            const SizedBox(height: 6),

            if (habilidades is List)
              Text(
                'Habilidades: '
                '${habilidades.join(', ')}',
              ),
          ],
        ),
      ),
    );
  }

  // =====================================================
  // BOTON REPORTE
  // =====================================================

  Widget construirBotonReporte() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: generandoReporte ? null : generarReportePDF,
        icon: generandoReporte
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              )
            : const Icon(Icons.picture_as_pdf),
        label: Text(
          generandoReporte ? 'Generando reporte...' : 'Generar reporte PDF',
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.red.shade600,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.all(15),
        ),
      ),
    );
  }

  // =====================================================
  // SELECTOR DE PAIS
  // =====================================================

  Widget construirSelectorPais() {
    return DropdownButtonFormField<String?>(
      value: paisSeleccionado,
      decoration: const InputDecoration(
        labelText: 'País de las ofertas',
        border: OutlineInputBorder(),
        prefixIcon: Icon(Icons.public),
      ),

      items: [
        const DropdownMenuItem<String?>(
          value: null,
          child: Text('Todos los países'),
        ),

        ...paises.entries.map((entrada) {
          return DropdownMenuItem<String?>(
            value: entrada.key,
            child: Text(entrada.key),
          );
        }),
      ],

      onChanged: (valor) {
        setState(() {
          paisSeleccionado = valor;
        });
      },
    );
  }

  // =====================================================
  // FILTRO REMOTO
  // =====================================================

  Widget construirFiltroRemoto() {
    return Card(
      child: CheckboxListTile(
        value: soloRemoto,

        onChanged: (valor) {
          setState(() {
            soloRemoto = valor ?? false;
          });
        },

        title: const Text('Solo empleos remotos'),

        subtitle: const Text(
          'Mostrar únicamente ofertas que '
          'permiten trabajar remotamente.',
        ),

        secondary: const Icon(Icons.home_work),

        controlAffinity: ListTileControlAffinity.trailing,
      ),
    );
  }

  // =====================================================
  // INTERFAZ
  // =====================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('JobHunter AI'),

        centerTitle: true,

        actions: [
          IconButton(
            onPressed: limpiarPantalla,
            tooltip: 'Limpiar pantalla',
            icon: const Icon(Icons.cleaning_services),
          ),

          IconButton(
            onPressed: abrirHistorial,
            tooltip: 'Historial',
            icon: const Icon(Icons.history),
          ),
        ],
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            // =========================================
            // TITULO
            // =========================================
            const Text(
              'Encuentra tu empleo ideal con IA',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 20),

            // =========================================
            // PAIS
            // =========================================
            construirSelectorPais(),

            const SizedBox(height: 10),

            // =========================================
            // REMOTO
            // =========================================
            construirFiltroRemoto(),

            const SizedBox(height: 10),

            // =========================================
            // CV
            // =========================================
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: analizandoCV ? null : seleccionarCV,

                icon: analizandoCV
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Icon(Icons.upload_file),

                label: Text(
                  analizandoCV ? 'Analizando CV...' : 'Seleccionar CV',
                ),

                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(15),
                ),
              ),
            ),

            const SizedBox(height: 10),

            // =========================================
            // BUSCAR
            // =========================================
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: cargando ? null : cargarEmpleos,

                icon: const Icon(Icons.search),

                label: const Text('Buscar empleos'),
              ),
            ),

            const SizedBox(height: 10),

            // =========================================
            // REPORTE
            // =========================================
            if (cvBytes != null) construirBotonReporte(),

            const SizedBox(height: 15),

            // =========================================
            // CONTENIDO
            // =========================================
            Expanded(
              child: ListView(
                children: [
                  // -------------------------------------
                  // CV
                  // -------------------------------------
                  if (cvNombre != null)
                    Card(
                      color: Colors.blue.shade50,
                      child: Padding(
                        padding: const EdgeInsets.all(12),
                        child: Row(
                          children: [
                            const Icon(Icons.description, color: Colors.blue),

                            const SizedBox(width: 10),

                            Expanded(
                              child: Text(
                                cvNombre!,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                  // -------------------------------------
                  // PERFIL
                  // -------------------------------------
                  construirPerfil(),

                  // -------------------------------------
                  // CARGANDO
                  // -------------------------------------
                  if (cargando || analizandoCV)
                    const Padding(
                      padding: EdgeInsets.all(20),
                      child: Center(child: CircularProgressIndicator()),
                    ),

                  // -------------------------------------
                  // SIN EMPLEOS
                  // -------------------------------------
                  if (empleos.isEmpty && !cargando && !analizandoCV)
                    const Padding(
                      padding: EdgeInsets.all(30),
                      child: Center(
                        child: Text(
                          'No hay empleos para mostrar.',
                          textAlign: TextAlign.center,
                        ),
                      ),
                    ),

                  // -------------------------------------
                  // EMPLEOS
                  // -------------------------------------
                  ...empleos.map((empleo) {
                    return JobCard(job: empleo);
                  }),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
