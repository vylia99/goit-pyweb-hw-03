import time
from multiprocessing import Pool, cpu_count

def factorize_number(n):
    return [i for i in range(1, n + 1) if n % i == 0]

# Синхронна версія
def factorize_sync(*numbers):
    results = []
    for n in numbers:
        results.append(factorize_number(n))
    return results

# Паралельна версія
def factorize_parallel(*numbers):
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(factorize_number, numbers)
    return results

if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060)

    print("== Синхронна версія ==")
    start_sync = time.time()
    a_sync, b_sync, c_sync, d_sync = factorize_sync(*numbers)
    end_sync = time.time()
    print(f"Час виконання (синхронно): {end_sync - start_sync:.4f} секунд\n")

    print("== Паралельна версія ==")
    start_parallel = time.time()
    a_par, b_par, c_par, d_par = factorize_parallel(*numbers)
    end_parallel = time.time()
    print(f"Час виконання (паралельно): {end_parallel - start_parallel:.4f} секунд\n")

    # Перевірка коректності
    assert a_sync == a_par
    assert b_sync == b_par
    assert c_sync == c_par
    assert d_sync == d_par

