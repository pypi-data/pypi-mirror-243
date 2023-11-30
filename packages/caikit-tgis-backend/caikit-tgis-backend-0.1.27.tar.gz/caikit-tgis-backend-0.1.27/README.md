# Caikit Text Generation Inference Service (TGIS) Backend

This project provides a Caikit module backend that manages models run in TGIS

## Configuration

Sample configuration using the `MULTI` finder and a remote `TGIS` backend):

```yaml
runtime:
  library: caikit_nlp
  local_models_dir: /path/to/models
  lazy_load_local_models: true

model_management:
  finders:
    default:
      type: MULTI
      config:
        finder_priority:
          - local
          - tgis-auto
  initializers:
    default:
      type: LOCAL
      config:
        backend_priority:
          - type: TGIS
            config:
              connection:
                hostname: "localhost:8033"
                test_connections: true
                connect_timeout: 30

log:
  formatter: pretty
```
