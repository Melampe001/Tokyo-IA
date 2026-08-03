package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "os"
    "time"
)

type BisiStream struct {
    Timestamp         string  `json:"timestamp"`
    BisiStatus        string  `json:"bisi_status"`
    HamiltonianEnergy string  `json:"hamiltonian_energy"`
    AlphaSignal       float64 `json:"alpha_signal"`
}

func main() {
    fmt.Println("[??] Iniciando puente Go del ecosistema BI-SI...")
    bridgeFile := "./bisi_stream.json"

    // Bucle de lectura de baja latencia (2ms) para capturar los datos de Python
    for i := 0; i < 5; i++ {
        if _, err := os.Stat(bridgeFile); err == nil {
            data, err := ioutil.ReadFile(bridgeFile)
            if err != nil {
                continue
            }

            var stream BisiStream
            json.Unmarshal(data, &stream)

            fmt.Printf("[???] BI-SI Data capturada -> Estado: %s | Señal Alfa: %.1f | Energía: %s\n", 
                stream.BisiStatus, stream.AlphaSignal, stream.HamiltonianEnergy)
            break
        }
        time.Sleep(2 * time.Millisecond) // Respetar el reloj de la suite de producción
    }
}
