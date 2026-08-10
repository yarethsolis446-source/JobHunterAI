import 'package:flutter/material.dart';

import '../models/job.dart';
import '../services/api_service.dart';
import '../widgets/job_card.dart';

class HistoryPage extends StatefulWidget {
  const HistoryPage({super.key});

  @override
  State<HistoryPage> createState() {
    return _HistoryPageState();
  }
}

class _HistoryPageState extends State<HistoryPage> {
  // =====================================================
  // VARIABLES
  // =====================================================

  List<Job> empleos = [];

  bool cargando = false;

  String? error;

  // =====================================================
  // INICIO
  // =====================================================

  @override
  void initState() {
    super.initState();

    cargarHistorial();
  }

  // =====================================================
  // CARGAR HISTORIAL
  // =====================================================

  Future<void> cargarHistorial() async {
    if (mounted) {
      setState(() {
        cargando = true;
        error = null;
      });
    }

    try {
      final datos = await ApiService.obtenerHistorial();

      if (!mounted) return;

      final resultados = datos
          .whereType<Map>()
          .map<Job>((json) => Job.fromJson(Map<String, dynamic>.from(json)))
          .toList();

      setState(() {
        empleos = resultados;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        error = e.toString();
      });
    } finally {
      if (mounted) {
        setState(() {
          cargando = false;
        });
      }
    }
  }

  // =====================================================
  // REFRESCAR
  // =====================================================

  Future<void> refrescar() async {
    await cargarHistorial();
  }

  // =====================================================
  // CARD VACÍA
  // =====================================================

  Widget construirVacio() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(30),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [
            Icon(Icons.history, size: 70, color: Colors.grey.shade400),

            const SizedBox(height: 15),

            const Text(
              "No hay empleos en el historial.",
              textAlign: TextAlign.center,

              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
            ),

            const SizedBox(height: 8),

            Text(
              "Los empleos recomendados "
              "aparecerán aquí después "
              "de analizar un CV.",

              textAlign: TextAlign.center,

              style: TextStyle(color: Colors.grey.shade600),
            ),

            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: cargarHistorial,

              icon: const Icon(Icons.refresh),

              label: const Text("Actualizar"),
            ),
          ],
        ),
      ),
    );
  }

  // =====================================================
  // ERROR
  // =====================================================

  Widget construirError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(30),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [
            const Icon(Icons.error_outline, size: 60, color: Colors.red),

            const SizedBox(height: 15),

            const Text(
              "No se pudo cargar el historial.",
              textAlign: TextAlign.center,

              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 10),

            Text(error ?? "Error desconocido", textAlign: TextAlign.center),

            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: cargarHistorial,

              icon: const Icon(Icons.refresh),

              label: const Text("Intentar nuevamente"),
            ),
          ],
        ),
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
        title: const Text("Historial"),

        centerTitle: true,

        actions: [
          IconButton(
            onPressed: cargando ? null : refrescar,

            tooltip: "Actualizar historial",

            icon: const Icon(Icons.refresh),
          ),
        ],
      ),

      body: cargando
          ? const Center(child: CircularProgressIndicator())
          : error != null
          ? construirError()
          : empleos.isEmpty
          ? construirVacio()
          : RefreshIndicator(
              onRefresh: refrescar,

              child: ListView(
                padding: const EdgeInsets.all(16),

                children: [
                  // =================================
                  // RESUMEN
                  // =================================
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),

                      child: Row(
                        children: [
                          const Icon(Icons.history, size: 30),

                          const SizedBox(width: 12),

                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,

                              children: [
                                const Text(
                                  "Empleos guardados",
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),

                                const SizedBox(height: 4),

                                Text(
                                  "${empleos.length} empleos en tu historial",
                                  style: TextStyle(color: Colors.grey.shade600),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 10),

                  // =================================
                  // EMPLEOS
                  // =================================
                  ...empleos.map((empleo) {
                    return JobCard(job: empleo);
                  }),
                ],
              ),
            ),
    );
  }
}
