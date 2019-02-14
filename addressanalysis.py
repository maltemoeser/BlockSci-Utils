import pandas as pd
import blocksci
from distutils.version import LooseVersion

if LooseVersion(blocksci.VERSION) < LooseVersion("0.6"):
    raise ImportError("Utils require BlockSci v0.6 or newer.")


def date_first_sent(addr):
    """
    First time an output associated with address `addr` is spent
    """
    return pd.to_datetime(addr.ins.block.time.min())


def date_last_sent(addr):
    """
    Last time an output associated with address `addr` is spent
    """
    # Time of last output associated with address being spent
    return pd.to_datetime(addr.ins.block.time.max())


def date_first_received(addr):
    """
    First time an output associated with address `addr` is created
    """
    return pd.to_datetime(addr.outs.block.time.min())


def date_last_received(addr):
    """
    Last time an output associated with address `addr` is created
    """
    return pd.to_datetime(addr.outs.block.time.max())


def time_active(addr, print_out=True):
    """
    Overview of the time period in which an address was active
    """
    start_time_in = date_first_sent(addr)
    start_time_out = date_last_sent(addr)
    end_time_in = date_first_received(addr)
    end_time_out = date_last_received(addr)

    if print_out:
        if start_time_out:
            print("Received coins between {} and {}.".format(start_time_out, end_time_out))
        else:
            print("Never received coins.")
        print()
        if start_time_in:
            print("Sent coins between {} and {}.".format(start_time_in, end_time_in))
        else:
            print("Never sent coins.")
    return ((start_time_out, end_time_out), (start_time_in, start_time_out))


def received_txes_without_change(addr):
    """
    Returns the transactions that send value to the address, excluding transactions that return change from outgoing payments
    """
    return addr.out_txes.where(lambda tx: ~tx.inputs.any(lambda i: i.address == addr))


def received_outs_without_change(addr):
    """
    Returns the outputs that send value to the address, excluding outputs in transactions that return change from outgoing payments
    """
    return addr.outs.where(lambda o: ~o.tx.inputs.any(lambda i: i.address == addr))
