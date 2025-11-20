from computational_models import State, TuringMachine


def double_ones_machine(x: int) -> TuringMachine:
    """
    This machine implements function f(x) = 2x, where x is a natural number.

    Tape is representation x on unary notation.
    """

    
    states = {
        "q1": State(
            {
                "0": ("0", 0, "halt"),
                "1": ("0", -1, "q2"),
            }
        ),
        "q2": State(
            {
                "0": ("1", 1, "q3"),
                "1": ("1", -1, "q2"),
            }
        ),
        "q3": State(
            {
                "0": ("1", 1, "q1"),
                "1": ("1", 1, "q3"),
            }
        ),

    }
    machine = TuringMachine(initial_state="q1", tape="1" * x, states=states)
    machine.run()

    return machine

if __name__ == "__main__":
    machine = double_ones_machine(2)
    machine.print_tape()
    machine.print_count_of_ones()
