import concurent_anything

test_iterable = ['The Neglected Holm', 'The Barnacle Key', 'The Dancing Enclave', 'The Peaceful Island',
                 'Allerport Reef', 'Cresstead Archipelago', 'Petromeny Islet', 'Esterisle Peninsula', 'Traygami Cay',
                 'Savaside Peninsula']


def reverse_function(string, start_index=0, end_index=-1, steps=1):
    return string[start_index:end_index:steps]


print(concurent_anything.MultiProcessAnything(test_iterable, reverse_function, args_tuple=(1,-1))())

