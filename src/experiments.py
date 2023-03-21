import concurent_anything

test_iterable = ['The Neglected Holm', 'The Barnacle Key', 'The Dancing Enclave', 'The Peaceful Island',
                 'Allerport Reef', 'Cresstead Archipelago', 'Petromeny Islet', 'Esterisle Peninsula', 'Traygami Cay',
                 'Savaside Peninsula']


def reverse_function(string):
    return string[::-1]


print(concurent_anything.MultiProcessAnything(test_iterable, reverse_function)())

