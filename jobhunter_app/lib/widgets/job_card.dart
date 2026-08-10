import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/job.dart';

class JobCard extends StatelessWidget {
  final Job job;

  const JobCard({super.key, required this.job});

  Color _colorScore() {
    if (job.score >= 80) {
      return Colors.green;
    }

    if (job.score >= 60) {
      return Colors.orange;
    }

    if (job.score >= 40) {
      return Colors.amber.shade700;
    }

    return Colors.red;
  }

  Future<void> _abrirOferta() async {
    if (job.link.isEmpty) {
      return;
    }

    final uri = Uri.tryParse(job.link);

    if (uri == null) {
      return;
    }

    await launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) {
    final color = _colorScore();

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // =========================================
            // TITULO
            // =========================================
            Text(
              job.titulo,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 5),

            Text(
              job.empresa,
              style: TextStyle(color: Colors.grey.shade700, fontSize: 15),
            ),

            const SizedBox(height: 12),

            // =========================================
            // SCORE
            // =========================================
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${job.score}%',
                    style: TextStyle(color: color, fontWeight: FontWeight.bold),
                  ),
                ),

                const SizedBox(width: 10),

                Expanded(
                  child: Text(
                    job.nivel,
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),

            // =========================================
            // DESCRIPCION
            // =========================================
            if (job.descripcion.isNotEmpty)
              Text(job.descripcion, style: const TextStyle(height: 1.4)),

            // =========================================
            // COINCIDENCIAS
            // =========================================
            if (job.coincidencias.isNotEmpty) ...[
              const SizedBox(height: 12),

              const Text(
                'Habilidades coincidentes',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),

              const SizedBox(height: 6),

              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: job.coincidencias
                    .map(
                      (skill) => Chip(
                        label: Text(skill),
                        backgroundColor: Colors.green.shade50,
                      ),
                    )
                    .toList(),
              ),
            ],

            // =========================================
            // FALTANTES
            // =========================================
            if (job.faltantes.isNotEmpty) ...[
              const SizedBox(height: 10),

              const Text(
                'Habilidades faltantes',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),

              const SizedBox(height: 6),

              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: job.faltantes
                    .map(
                      (skill) => Chip(
                        label: Text(skill),
                        backgroundColor: Colors.red.shade50,
                      ),
                    )
                    .toList(),
              ),
            ],

            // =========================================
            // UBICACION
            // =========================================
            if (job.ubicacion.isNotEmpty) ...[
              const SizedBox(height: 8),

              Row(
                children: [
                  const Icon(Icons.location_on, size: 18),
                  const SizedBox(width: 5),
                  Text(job.ubicacion),
                ],
              ),
            ],

            // =========================================
            // SALARIO
            // =========================================
            if (job.salario.isNotEmpty) ...[
              const SizedBox(height: 5),

              Row(
                children: [
                  const Icon(Icons.attach_money, size: 18),
                  const SizedBox(width: 5),
                  Text(job.salario),
                ],
              ),
            ],

            const SizedBox(height: 12),

            // =========================================
            // BOTON
            // =========================================
            if (job.link.isNotEmpty)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _abrirOferta,
                  icon: const Icon(Icons.open_in_new),
                  label: const Text('Ver oferta'),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
