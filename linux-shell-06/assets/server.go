package main
import (
    "fmt"
    "net/http"
)
type msg string
func (m msg) ServeHTTP(resp http.ResponseWriter, req *http.Request) {
   fmt.Fprint(resp, m)
}
func main() {
    msgHandler := msg("Простой web-сервер\n")
    http.ListenAndServe("localhost:80", msgHandler)
}