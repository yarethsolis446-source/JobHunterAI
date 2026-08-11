import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

class ApiService {
  // =====================================================
  // URL DEL BACKEND
  // =====================================================

  static const String baseUrl = 'https://jobhunterai-tmku.onrender.com';
  // =====================================================
  // OBTENER EMPLEOS
  // =====================================================

  static Future<List<dynamic>> obtenerEmpleos(
    String consulta, {
    String? pais,
    bool remoto = false,
  }) async {
    final parametros = <String, String>{
      'consulta': consulta,
      'remoto': remoto.toString(),
    };

    if (pais != null && pais.isNotEmpty) {
      parametros['pais'] = pais;
    }

    final uri = Uri.parse('$baseUrl/jobs').replace(queryParameters: parametros);

    try {
      final response = await http.post(uri);

      if (response.statusCode != 200) {
        throw Exception(
          'Error obteniendo empleos: '
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

      final empleos = data['empleos'];

      if (empleos is! List) {
        return [];
      }

      return empleos;
    } catch (e) {
      if (e is Exception && e.toString().contains('Error obteniendo empleos')) {
        rethrow;
      }

      throw Exception('No se pudo conectar con el backend:\n$e');
    }
  }

  // =====================================================
  // ANALIZAR CV
  // =====================================================

  static Future<Map<String, dynamic>> analizarCV(
    String nombreArchivo,
    Uint8List archivo, {
    String? pais,
    bool remoto = false,
  }) async {
    final uri = Uri.parse('$baseUrl/upload-cv');

    try {
      final request = http.MultipartRequest('POST', uri);

      request.fields['pais'] = pais ?? '';
      request.fields['remoto'] = remoto.toString();

      request.files.add(
        http.MultipartFile.fromBytes(
          'archivo',
          archivo,
          filename: nombreArchivo,
        ),
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
    } catch (e) {
      if (e is Exception && e.toString().contains('Error analizando CV')) {
        rethrow;
      }

      throw Exception('No se pudo analizar el CV:\n$e');
    }
  }

  // =====================================================
  // GENERAR REPORTE PDF
  // =====================================================

  static Future<Uint8List> generarReportePDF(
    String nombreArchivo,
    Uint8List archivo,
  ) async {
    final uri = Uri.parse('$baseUrl/generate-report');

    try {
      final request = http.MultipartRequest('POST', uri);

      request.files.add(
        http.MultipartFile.fromBytes(
          'archivo',
          archivo,
          filename: nombreArchivo,
        ),
      );

      final streamedResponse = await request.send();

      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode != 200) {
        throw Exception(
          'Error generando reporte PDF: '
          '${response.statusCode}\n'
          '${response.body}',
        );
      }

      return response.bodyBytes;
    } catch (e) {
      if (e is Exception &&
          e.toString().contains('Error generando reporte PDF')) {
        rethrow;
      }

      throw Exception('No se pudo generar el reporte PDF:\n$e');
    }
  }

  // =====================================================
  // HISTORIAL
  // =====================================================

  static Future<List<dynamic>> obtenerHistorial() async {
    final uri = Uri.parse('$baseUrl/history');

    try {
      final response = await http.get(uri);

      if (response.statusCode != 200) {
        throw Exception(
          'Error obteniendo historial: '
          '${response.statusCode}\n'
          '${response.body}',
        );
      }

      final data = jsonDecode(response.body);

      if (data is! Map<String, dynamic>) {
        throw Exception('Respuesta inválida del servidor');
      }

      final empleos = data['empleos'];

      if (empleos is! List) {
        return [];
      }

      return empleos;
    } catch (e) {
      throw Exception('No se pudo obtener el historial:\n$e');
    }
  }

  // =====================================================
  // OBTENER EMPLEO DEL HISTORIAL
  // =====================================================

  static Future<Map<String, dynamic>> obtenerEmpleoHistorial(
    String jobId,
  ) async {
    final uri = Uri.parse('$baseUrl/history/$jobId');

    try {
      final response = await http.get(uri);

      if (response.statusCode != 200) {
        throw Exception(
          'Error obteniendo empleo del historial: '
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
    } catch (e) {
      throw Exception('No se pudo obtener el empleo:\n$e');
    }
  }
}
