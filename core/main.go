package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "os/exec"
)

type AgentContext struct {
    SystemStatus string   `json:"system_status"`
    ActiveModels []string `json:"active_models"`
    LastSync     string   `json:"last_sync"`
}

func main() {
    fmt.Println("[??] Inicializando Puente de Comunicación Go <-> GGUF Core Engine")

    // Leer matriz de aprendizaje local antes de interactuar con el modelo
    matrixPath := "../trig_rules/agents_learning_matrix.json"
    fileData, err := ioutil.ReadFile(matrixPath)
    if err != nil {
        log.Println("[??] No se pudo leer la matriz de aprendizaje. Usando contexto base.")
    }

    var ctx AgentContext
    json.Unmarshal(fileData, &ctx)

    fmt.Printf("[???] Modelos activos cargados en memoria: %v\n", ctx.ActiveModels)
}

// ExecutePowerShell encapsula llamadas seguras de los agentes al sistema operativo
func ExecutePowerShell(command string) (string, error) {
    cmd := exec.Command("powershell", "-Command", command)
    var out bytes.Buffer
    cmd.Stdout = &out
    err := cmd.Run()
    if err != nil {
        return "", err
    }
    return out.String(), nil
}
