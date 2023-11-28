"""
Ensure you have a modbus slave available with specified parameters for this test.
( I used pyModSlave )
"""
import asyncio

from iot_protocols.modbus import ModbusClient, AsyncModbusClient, request_factory, requests



RCS={
        "function": "ReadCoils",
        "unit": 1,
        "address": 5,
        "count": 4
    }
WCS={
        "function": "WriteCoils",
        "unit": 1,
        "address": 5,
        "values": [True]*5

    }
RDI={
        "function": "ReadDiscreteInput",
        "unit": 1,
        "address": 0,
        "count": 5
    }
RIR={
        "function": "ReadInputRegister",
        "unit": 1,
        "address": 10,
        "count": 3,
        "encoding": "int64"
    }
RHR={
        "function": "ReadHoldingRegister",
        "unit": 1,
        "address": 1,
        "count": 3,
        "encoding": "int64"
    }

SERIAL_CLIENT = ModbusClient.with_serial_client(
        port="COM11",
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=5
    )
TCP_CLIENT = ModbusClient.with_tcp_client(
        host="127.0.0.1",
        port=502
    )

COILS = [True, False, True, False, True]
DI = [not c for c in COILS]
IR = [28,11,1996]
HR = [28,11,1996]

def test_serial_client():
    rcs = request_factory(RCS)
    assert isinstance(rcs, requests.ReadCoils)
    expected_coils = SERIAL_CLIENT.request(rcs)
    assert expected_coils == COILS
    NEW_COILS = [True]*5
    wcs = request_factory(WCS)
    new_coils = SERIAL_CLIENT.request(wcs)
    assert new_coils == wcs.values
