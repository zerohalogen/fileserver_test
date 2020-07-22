# Простой сервер для хранения файлов

## Описание:
Так как в ТЗ не были указаны детали реализации, чтобы не изобретать велосипед и облегчить задачу, было решено использовать fastapi

## Запуск сервера:
```
uvicorn main:app
```
Сервер доступен по адресу localhost:8000, Swagger UI - localhost:8000/docs

## Доступные методы:

### POST /upload
```
curl -X POST "http://localhost:8000/upload/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@<загружаемый-файл>"
```
Пример ответа:
```
{
  "hash": "f83c7ee7560ae93fdad36318a15f21409e5e58f12d9ee4fd4a1d677daf0bc9c8"
}
```
Где значение - хэш загружаемого файла

### DELETE /delete
```
curl -X DELETE "http://127.0.0.1:8000/delete/?filename=<хэш-файла>" -H  "accept: application/json"
```
Пример ответа, если файл был найден и удален:
```
{
  "File was deleted: ": "f83c7ee7560ae93fdad36318a15f21409e5e58f12d9ee4fd4a1d677daf0bc9c8"
}
```
если файл не был найден:
```
{
   "File was not found: ": "f83c7ee7560ae93fdad46318a15f21409e5e58f12d9ee4fd4a1d677daf0bc9c8"
}
```
Если директория, в которой находился удаляемый файл пуста, она также удаляется

### GET /download
```
curl -X GET "http://127.0.0.1:8000/download/?filename=<хэш-файла>" -H  "accept: application/json"
```
Если файл не был найден, вернет:
```
{
  "File was not found: ": "f83c7ee7560ae93fdad46318a15f21409e5e58f12d9ee4fd4a1d677daf0bc9c8"
}
```
В случае успеха вернет файл для скачивания.