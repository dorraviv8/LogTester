{{- define "logtester-api.name" -}}
logtester-api
{{- end -}}

{{- define "logtester-api.fullname" -}}
{{ include "logtester-api.name" . }}
{{- end -}}

