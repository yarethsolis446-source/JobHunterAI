class Job {
  final String jobId;
  final String titulo;
  final String empresa;
  final String descripcion;
  final List<String> habilidades;
  final int experiencia;
  final String link;
  final String ubicacion;
  final String salario;
  final String idioma;
  final String nivel;
  final bool remoto;
  final String tipoEmpleo;
  final String pais;

  int score;
  List<String> coincidencias;
  List<String> faltantes;
  List<String> explicacion;

  String fechaEncontrado;

  Job({
    this.jobId = '',
    this.titulo = '',
    this.empresa = '',
    this.descripcion = '',
    this.habilidades = const [],
    this.experiencia = 0,
    this.link = '',
    this.ubicacion = '',
    this.salario = '',
    this.idioma = '',
    this.nivel = '',
    this.remoto = false,
    this.tipoEmpleo = '',
    this.pais = '',
    this.score = 0,
    this.coincidencias = const [],
    this.faltantes = const [],
    this.explicacion = const [],
    this.fechaEncontrado = '',
  });

  factory Job.fromJson(Map<String, dynamic> json) {
    return Job(
      jobId: (json['job_id'] ?? json['id'] ?? '').toString(),

      titulo: (json['titulo'] ?? '').toString(),

      empresa: (json['empresa'] ?? '').toString(),

      descripcion: (json['descripcion'] ?? '').toString(),

      habilidades: _convertirLista(json['habilidades']),

      experiencia: _convertirInt(json['experiencia']),

      link: (json['link'] ?? '').toString(),

      ubicacion: (json['ubicacion'] ?? '').toString(),

      salario: (json['salario'] ?? '').toString(),

      idioma: (json['idioma'] ?? '').toString(),

      nivel: (json['nivel'] ?? '').toString(),

      remoto: _convertirBool(json['remoto']),

      tipoEmpleo: (json['tipo_empleo'] ?? '').toString(),

      pais: (json['pais'] ?? '').toString(),

      score: _convertirInt(json['score']),

      coincidencias: _convertirLista(json['coincidencias']),

      faltantes: _convertirLista(json['faltantes']),

      explicacion: _convertirLista(json['explicacion']),

      fechaEncontrado: (json['fecha_encontrado'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'job_id': jobId,
      'titulo': titulo,
      'empresa': empresa,
      'descripcion': descripcion,
      'habilidades': habilidades,
      'experiencia': experiencia,
      'link': link,
      'ubicacion': ubicacion,
      'salario': salario,
      'idioma': idioma,
      'nivel': nivel,
      'remoto': remoto,
      'tipo_empleo': tipoEmpleo,
      'pais': pais,
      'score': score,
      'coincidencias': coincidencias,
      'faltantes': faltantes,
      'explicacion': explicacion,
      'fecha_encontrado': fechaEncontrado,
    };
  }

  static List<String> _convertirLista(dynamic valor) {
    if (valor is List) {
      return valor.map((e) => e.toString()).toList();
    }

    return [];
  }

  static int _convertirInt(dynamic valor) {
    if (valor is int) {
      return valor;
    }

    if (valor is double) {
      return valor.toInt();
    }

    if (valor is String) {
      return int.tryParse(valor) ?? 0;
    }

    return 0;
  }

  static bool _convertirBool(dynamic valor) {
    if (valor is bool) {
      return valor;
    }

    if (valor is String) {
      return valor.toLowerCase() == 'true';
    }

    if (valor is int) {
      return valor == 1;
    }

    return false;
  }
}
