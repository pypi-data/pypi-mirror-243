import json
import logging
import os
import time
from pathlib import Path
from typing import List, Union

import requests
from qiskit import QuantumCircuit, qasm3
from qiskit.qasm2 import QASM2ExportError

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BackendTaskError(Exception):
    def __init__(self, status: str, msg: str):
        self.status = status
        self.msg = msg


class TranspilerServiceAPI:
    """A helper class that covers some basic funcionality from the Qiskit Transpiler API"""

    def __init__(self, url: str = None, token: str = None):
        # If it does not recive URL or token, the function tries to find your Qiskit
        # token from the QISKIT_IBM_TOKEN env var
        # If it couldn't find it, it will try to get it from your ~/.qiskit/qiskit-ibm.json file
        # If it couldn't find it, it fails

        if url is None:
            self.url = os.environ.get(
                "QISKIT_TRANSPILER_SERVICE_URL",
                "https://cloud-transpiler-experimental.quantum-computing.ibm.com/",
            )
        else:
            self.url = url

        if token is None:
            token = os.environ.get("QISKIT_IBM_TOKEN")

            if token is None:
                with open(Path.home() / ".qiskit" / "qiskit-ibm.json", "r") as _sc:
                    creds = json.loads(_sc.read())
                token = creds.get("default-ibm-quantum", {}).get("token")
                if token is None:
                    logging.warning("The token is undefined")
        else:
            self.token = token

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def get_versions(self):
        url = f"{self.url}/version"
        resp = requests.get(
            url,
            headers=self.headers,
        ).json()

        return resp

    def transpile(
        self,
        circuits: Union[
            Union[List[str], str], Union[List[QuantumCircuit], QuantumCircuit]
        ],
        optimization_level: int = 1,
        backend: Union[str, None] = None,
        coupling_map: Union[List[List[int]], None] = None,
        ai: bool = True,
        qiskit_transpile_options: dict = None,
    ):
        if type(circuits) is QuantumCircuit:
            qasm = circuits.qasm().replace("\n", " ")
        elif type(circuits) is List[QuantumCircuit]:
            qasm = []
            for circuit in circuits:
                qasm.append(circuit.qasm().replace("\n", " "))
        elif type(circuit) is str:
            qasm = circuit.replace("\n", " ")
        else:
            # The type should be List[str]
            qasm = []
            for circuit in circuits:
                qasm = circuit.replace("\n", " ")

        json_args = {
            "qasm_circuits": qasm,
        }

        if qiskit_transpile_options is not None:
            json_args["qiskit_transpile_options"] = qiskit_transpile_options
        if coupling_map is not None:
            json_args["backend_coupling_map"] = coupling_map

        params = {
            "backend": backend,
            "optimization_level": optimization_level,
            "use_ai": ai,
        }

        transpile_resp = self.request_and_wait(
            endpoint="transpile", body=json_args, params=params
        )

        if transpile_resp.get("success"):
            transpiled_circuit = QuantumCircuit.from_qasm_str(transpile_resp["qasm"])
            return transpiled_circuit

    def benchmark(
        self,
        circuits: Union[
            Union[List[str], str], Union[List[QuantumCircuit], QuantumCircuit]
        ],
        backend: str,
        optimization_level: int = 1,
        qiskit_transpile_options: dict = None,
    ):
        raise Exception("Not implemented")

    def request_and_wait(self, endpoint: str, body: dict, params: dict):
        resp = requests.post(
            f"{self.url}/{endpoint}",
            headers=self.headers,
            json=body,
            params=params,
        ).json()

        task_id = resp.get("task_id")

        result = BackendTaskError(
            status="PENDING", msg=f"The background task {task_id} timed out"
        )
        for _ in range(20):
            resp = requests.get(
                url=f"{self.url}/{endpoint}/{task_id}", headers=self.headers
            ).json()
            if resp.get("state") == "PENDING":
                time.sleep(1)
            elif resp.get("state") == "SUCCESS":
                result = resp.get("result")
                break
            elif resp.get("state") == "FAILURE":
                logging.error("The request FAILED")
                result = BackendTaskError(
                    status="FAILURE", msg=f"The background task {task_id} FAILED"
                )
                break

        if isinstance(result, BackendTaskError):
            logging.error(f"Failed to get an result for {endpoint}: {result.msg}")
            raise result
        else:
            return result
