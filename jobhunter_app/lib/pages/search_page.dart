import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

class ApiService {
  // =====================================================
  // URL DEL BACKEND
  // =====================================================

  static const String baseUrl = 'http://127.0.0.1:8000';

  // =====================================================
  // OBTENER EMPLEOS
  // =====================================================

  Future<List<dynamic>> obtenerEmpleos() async {
    final uri = Uri.parse('$baseUrl/jobs');

    final response = await http.post(uri);

    if (response.statusCode != 200) {
      throw Exception(
        'Error obteniendo empleos: '
        '${response.statusCode}',
      );
    }

    final data = jsonDecode(response.body);

    if (data is! Map<String, dynamic>) {
      throw Exception('Respuesta inválida del servidor');
    }

    if (data['error'] != null) {
      throw Exception(data['error'].toString());
    }

    return data['empleos'] ?? [];
  }

  // =====================================================
  // ANALIZAR CV
  // =====================================================

  Future<Map<String, dynamic>> analizarCV(
    String nombreArchivo,
    Uint8List archivo,
  ) async {
    final uri = Uri.parse('$baseUrl/upload-cv');

    final request = http.MultipartRequest('POST', uri);

    request.files.add(
      http.MultipartFile.fromBytes('archivo', archivo, filename: nombreArchivo),
    );

    final streamedResponse = await request.send();

    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode != 200) {
      throw Exception(
        'Error analizando CV: '
        '${response.statusCode}\n'
        '${response.body}',
      );
    }

    final data = jsonDecode(response.body);

    if (data is! Map<String, dynamic>) {
      throw Exception('Respuesta inválida del servidor');
    }

    if (data['error'] != null) {
      throw Exception(data['error'].toString());
    }

    return data;
  }
}
