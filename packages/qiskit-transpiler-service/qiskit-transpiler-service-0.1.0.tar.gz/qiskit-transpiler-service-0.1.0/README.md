# qiskit-ai-transpiler-plugin

A custom synthesis plugin for Qiskit transpiler that uses the qiskit_transpiler_service service <https://clifford-ai-experimental.quantum-computing.ibm.com/docs>

## Installing the plugin

Before using the plugin, you need to install it, so Qiskit could collect it and use it as a transpiler plugin. To install the plugin, please run:

```sh
!pip install -e .
```

## Authentication

This plugin uses the same token as IBM Quantum Platform to authenticate (it authenticates directly against its API). So, for authenticating yourself and use the underlying service please use any of these two options to store the IQP token:

- You have the token in your `~/.qiskit/qiskit-ibm.json`. For more information about how to store the token in the file, please check [the instructions on the qiskit-ibm-provider repo](https://github.com/Qiskit/qiskit-ibm-provider/#provider-setup)
- You have the token in the `QISKIT_IBM_TOKEN` environment variable.

If you are going to use other instance of our service that is not the current one <https://clifford-ai-experimental.quantum-computing.ibm.com>, you can set up a different URL via setting up the `CLIFFORDAI_URL` env var.

## Verify the plugin is available via Qiskit

Once you have installed the plugin, Qiskit should collect it and know it's available to be used with its transpiled methods.

To assert the plugin is recognized and available to be used with Qiskit, you can run:

```python
from qiskit.transpiler.passes.synthesis.plugin import HighLevelSynthesisPluginManager

hl_synth_plugin_manager = HighLevelSynthesisPluginManager()
plugin_names = hl_synth_plugin_manager.plugins.names()
assert "clifford.ai" in plugin_names
```

## How to use the plugin?

After check the plugin is available, you can use it with Qiskit transpile as follows:

```python

# Instantiate the plugin

from qiskit.transpiler.passes.synthesis import HLSConfig
from qiskit_transpiler_service import qiskit_transpiler_serviceSynthesizer
from qiskit_transpiler_service import HighLevelSynthesis

clifford_synth = qiskit_transpiler_serviceSynthesizer(backend="kolkata")
clifford_transpiler_pass = HighLevelSynthesis(HLSConfig(clifford=[clifford_synth]))  # The clifford transpiler pass

# Define your circuit including Cliffords

import random
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford

qc1 = QuantumCircuit(27)

clifford_locations = [
    [4,7,10,12,15,18,13],
    [10,12,15,13,11,14,16],
    [0,1,4,7,2,3,5],
    [3,5,8,11,9],
    [17,18,21,23,24,25,26,22],
    [16,19,20,22]
]

# 10 layers of cliffords + non-cliffords
for _ in range(10):
    # 5 cliffords per layer
    qargs = random.choice(clifford_locations)
    qc1.append(random_clifford(len(qargs)), qargs)
    for qi in qargs:
        qc1.u(random.random(), random.random(), random.random(), qi)
    #qc1.barrier()

# Draw the circuit (optional)
qc1.draw(fold=-1)

# Transpile the circuit using the Clifford AI plugin

from qiskit import transpile
from qiskit_transpiler_service import get_metrics
from qiskit.providers.fake_provider import FakeKolkataV2

qc1_ai = clifford_transpiler_pass(qc1)
print(get_metrics(qc1_ai))

# Draw the resulting circuit
qc1_ai.draw(fold=-1)
```

More details and differences versus the common Qiskit transpiler passes are available in the [demo notebook](demo.ipynb).
