import math


def find_primes(start: int, end: int):
    """
    Finds prime numbers in the range and
    records steps explaining break/continue/for-else.
    """

    primes = []
    steps = []

    for n in range(start, end + 1):

        # CONTINUE example
        if n > 2 and n % 2 == 0:
            steps.append({
                "number": n,
                "action": "continue",
                "reason": f"{n} is even → skipped",
                "is_prime": False
            })
            continue

        # Check divisors
        for divisor in range(2, int(math.sqrt(n)) + 1):

            if n % divisor == 0:
                # BREAK example
                steps.append({
                    "number": n,
                    "action": "break",
                    "reason": f"{n} divisible by {divisor}",
                    "is_prime": False
                })
                break

        else:
            # FOR-ELSE example
            if n >= 2:
                primes.append(n)

                steps.append({
                    "number": n,
                    "action": "prime",
                    "reason": "no divisor found → prime",
                    "is_prime": True
                })

    return primes, steps