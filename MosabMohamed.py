from mido import MidiFile
from mido import MidiTrack
from mido import Message
from music21.converter import parse
import random
import numpy as np

# Global variables
quarter_time = 384

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_to_midi_number(note, octave):
    """
    This function is used to convert a note and an octave to a MIDI number

    Each octave contains 12 notes
    Each octave starts with the note C

    We treat enharmonic keys as the same key because they include the same physical notes and
    sequence of MIDI values in the same order. e.g.(C# and Dflat))

    MIDI values of notes is equal to : (((octaveNumber)*12) + (noteNumber))
    we use noteNumber with 0 base, where C = 0 and B = 11

    e.g. note G5 = (((5)*12) + 7) = ((5*12) + 7) = 60+7 = 67

    :param note: string: contains the note name in capital letters
    :param octave: integer: contains the octave of the note
    :return: integer: follows this formula ((octaveNumber*12) + (noteNumber))
    """
    note_number = 0
    for i in range(len(notes)):
        if note == notes[i]:
            note_number = i
            break
    return (octave * 12) + note_number


def midi_number_to_note(midi_number):
    """
    This function is used to convert a MIDI number to a note and an octave

    MIDI values of notes is equal to : (((octaveNumber)*12) + (noteNumber))
    we use noteNumber with 0 base, where C = 0 and B = 11

    e.g. note G5 = (((5)*12) + 7) = ((5*12) + 7) = 60+7 = 67

    so based on that we can get the octave number based on how many 12s are in the midi number,
    and we can get the note number in the octave with midi_number-(octave_number*12)

    e.g. midi_number = 67
    int(67/12) = 5 <-- the octave number
    67-60 = 7 <-- the note number
    the seventh note is G
    Therefore midi(67) = G5

    :param midi_number: integer: represents the midi_number
    :return: list[int,int] that represents [note_name, octave_number]
    """
    octave = int(midi_number / 12)
    note_number = midi_number - (octave * 12)
    note = notes[note_number]
    return [note, octave]


def major_triad(root_midi):
    """
    This function is used to create a major triad chord based on a root

    A major triad chord is represented in the integer notation as {0,4,7}
    Where each number refers to the distance between the note and the root note
    e.g. C major triad will be {C,E,G}
      which has the root note C
      and based on the order of notes: {C,C#,D,D#,E,F,F#,G,G#,A,A#,B}
      E is the fourth key from C
      G is the seventh key from C

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi, root_midi + 4, root_midi + 7]
    return chord


def minor_triad(root_midi):
    """
    This function is used to create a minor triad chord based on a root

    A minor triad chord is represented in the integer notation as {0,3,7}

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi, root_midi + 3, root_midi + 7]
    return chord


def first_inverted_major(root_midi):
    """
    This function is used to create a first inverted major chord based on a root

    A first inverted major chord is represented in the integer notation as {12,4,7}
    where the root refers to 0 in integer notation

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi + 12, root_midi + 4, root_midi + 7]
    return chord


def first_inverted_minor(root_midi):
    """
    This function is used to create a first inverted minor chord based on a root

    A first inverted minor chord is represented in the integer notation as {12,3,7}
    where the root refers to 0 in integer notation

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi + 12, root_midi + 3, root_midi + 7]
    return chord


def second_inverted_major(root_midi):
    """
    This function is used to create a second inverted major chord based on a root

    A second inverted major chord is represented in the integer notation as {12,16,7}
    where the root refers to 0 in integer notation

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi + 12, root_midi + 16, root_midi + 7]
    return chord


def second_inverted_minor(root_midi):
    """
    This function is used to create a second inverted minor chord based on a root

    A second inverted minor chord is represented in the integer notation as {12,15,7}
    where the root refers to 0 in integer notation

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi + 12, root_midi + 15, root_midi + 7]
    return chord


def diminished(root_midi):
    """
    This function is used to create a diminished chord based on a root

    A diminished chord is represented in the integer notation as {0,3,6}

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi, root_midi + 3, root_midi + 6]
    return chord


def sus2(root_midi):
    """
    This function is used to create a suspended second chord based on a root

    A suspended second chord triad chord is represented in the integer notation as {0,2,7}

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi, root_midi + 2, root_midi + 7]
    return chord


def sus4(root_midi):
    """
    This function is used to create a suspended fourth chord based on a root

    A suspended fourth chord is represented in the integer notation as {0,5,7}

    refer to the comments above the function major_triad to understand the integer notation

    :param root_midi: integer: represents the MIDI number of the root note
    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [root_midi, root_midi + 5, root_midi + 7]
    return chord


def rest():
    """
    This function is used to create a rest.

    A rest is where nothing is played

    :return: list[int,int,int]: each integer refers to the MIDI number of a specific note
    """
    chord = [-1, -1, -1]
    return chord


def parse_input(input_mid):
    """
    This function is used to parse input midi file and,
    return the important information,
    which is the note played and the time it was played for

    :param input_mid: mido.Midifile: that contains the midi file we want to parse
    :return: list[int,int]: that contains the note played and the time it was played for
    """
    pressed_keys = []
    for track in input_mid.tracks:
        for msg in track:
            if msg.type == "note_on" and msg.time != 0:
                pressed_keys.append([0, msg.time])
            elif msg.type == "note_off" and msg.time != 0:
                pressed_keys.append([msg.note, msg.time])
    return pressed_keys


def get_averages(notes_and_times):
    """
    This function is used to take some notes that were played on a set interval,
    and it calculates the average note played in that interval
    by multiplying each note played to its percentage time played in the interval

    :param notes_and_times: list[int,int]: that contains the note played and the time it was played for
    :return: float: that is the average note played over an interval of time
    """
    average = 0.0
    total_time = 0
    for j in range(len(notes_and_times)):
        total_time = total_time + notes_and_times[j][1]
    for j in range(len(notes_and_times)):
        average = average + (notes_and_times[j][0] * (notes_and_times[j][1] / total_time))
    return average


def average_notes(original_melody):
    """
    This function is used to get a list with the average notes played in each quarter of a bar
    by going through each note played from the input and adding it to a new list then
    when we reach the point of completing a quarter of a bar time, we call the function get_average,
    and we pass to it the notes played in the previous quarter and its times
    which will return a float value of the average note played over that quarter, then we append it to the final output

    :param original_melody: list[int,int]: that contains the note played and the time it was played for
    :return: list[float]: that contains the average note played in each quarter of a bar in the input
    """
    ret = []
    averages = []
    time = 0

    for i in range(len(original_melody)):
        time = time + original_melody[i][1]
        if original_melody[i][0] == 0:
            continue
        if time < quarter_time:
            averages.append(original_melody[i])
        if time == quarter_time:
            averages.append(original_melody[i])
            ret.append(get_averages(averages))
            averages = []
            time = 0
        if time >= quarter_time:
            averages.append([original_melody[i][0], original_melody[i][1] - (time - quarter_time)])
            ret.append(get_averages(averages))
            time = original_melody[i][1] - (averages[len(averages) - 1][1])
            if time >= quarter_time:
                while True:
                    ret.append(float(original_melody[i][0]))
                    time = time - quarter_time
                    if time < quarter_time:
                        break
            averages = []
            if time != 0:
                averages.append([original_melody[i][0], time])
    for avg in range(len(ret)):
        ret[avg] = ret[avg] - 24
    return ret


def create_population(size, length):
    """
    This function creates a random population, that consists of random individuals
    Each individual consists of some number of chords
    Each chord is generated based on a random root note

    :param size: integer: the size of the population
    :param length: integer: the number of chords in each individual
    :return: list[list[int,int,int]]: a random population consisting of random individuals consisting of random chords
    """
    population = []
    for i in range(size):
        individual = []
        for j in range(length):
            individual.append(random.choice([
                major_triad(random.randint(0, 110)),
                minor_triad(random.randint(0, 110)),
                first_inverted_major(random.randint(0, 110)),
                first_inverted_minor(random.randint(0, 110)),
                second_inverted_major(random.randint(0, 110)),
                second_inverted_minor(random.randint(0, 110)),
                sus2(random.randint(0, 110)),
                sus4(random.randint(0, 110)),
                diminished(random.randint(0, 110)),
                rest()
            ]))
        population.append(individual)
    return population


def similarity_to_original_melody(individual, target):  # change numbers
    """
    This function is a part of the fitness function that calculates a score for an individual
    based on how similar it is to the average notes played in each quarter in the original melody.
    It does that based on how far each note for the chord to the average note played in that specific quarter.
    Where the weight of the mediant is 50% and tonic is 25% and dominant is 25%

    :param individual: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes
    :param target: list[float]: the average notes played in each quarter of a bar in the original melody
    :return: float: the similarity score for the individual
    """
    score = 0
    for i in range(min(len(individual), len(target))):
        tonic = individual[i][0]
        mediant = individual[i][1]
        dominant = individual[i][2]
        diff_ton = abs(float(target[i]) - float(tonic))
        diff_med = abs(float(target[i]) - float(mediant))
        diff_dom = abs(float(target[i]) - float(dominant))
        diff1 = max(10.0 - diff_ton, 0.0)
        diff2 = max(10.0 - diff_med, 0.0)
        diff3 = max(10.0 - diff_dom, 0.0)
        diff = diff2 * 10 + diff1 * 5 + diff3 * 5
        score = score + diff
    return score


def chord_exists(individual, possible_chords):
    """
    This function is a part of the fitness function that calculates a score for an individual
    based on if the chords in that individual are valid chords or not.
    It does that based on the rule that each chord based on a specific key must be consisting of three notes
    where the first note is the root note and can be any note from the possible notes to compose a chord form the key.
    And the second note should be a note from the possible notes to compose a chord that is after the first note
    with two cells.
    And the third note should be a note from the possible notes to compose a chord that is after the second note
    with two cells.

    e.g.
    if we have C Major as the melody key,
    then we have the possible notes to compose a chord are: ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    and a valid chord based on the root note C would be C - E - G.
    all the valid chords are {[CEG],[DFA],[EGB],[FAC],[GBC],[ACE],[BDF]}

    :param individual: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes
    :param possible_chords: list[char]: the possible notes to compose a chord from in the original melody's key
    :return: float: the chords score for the individual
    """
    score = 0
    for i in range(len(individual)):
        tonic = individual[i][0] % 12
        mediant = individual[i][1] % 12
        dominant = individual[i][2] % 12
        possible = False
        for j in range(len(possible_chords)):
            x = note_to_midi_number(possible_chords[(j + 0) % 7], 0)
            y = note_to_midi_number(possible_chords[(j + 2) % 7], 0)
            z = note_to_midi_number(possible_chords[(j + 4) % 7], 0)
            if tonic == x and y == mediant and z == dominant:
                score = score + 100
                possible = True
                break
        if not possible:
            score = score - 100
    return score


def redundant_chords(individual):
    """
    This function is a part of the fitness function that calculates a score for an individual
    based on how the chord is placed relative to the previous score.
    It does that by checking each chord and the previous two chords,
    and if the current chord is the same as the previous chord we reward this individual
    but if the current chord is the same as the previous chord we punish this individual

    our target is to have the individual consisting of pairs of chords that are the same chord, to have a good flow
    throughout the melody

    :param individual: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes
    :return: float: the redundancy score for the individual
    """
    score = 0
    for i in range(len(individual)):
        if i >= 2:
            redundant = True
            for j in range(len(individual[i])):
                first = individual[i - 2][0]
                second = individual[i - 1][0]
                third = individual[i][0]
                if first != second or first != third or second != third:
                    redundant = False
            if redundant:
                score = score - 100
            else:
                score = score + 100
        if i >= 1:
            pair = True
            for j in range(len(individual[i])):
                first = individual[i - 1][0]
                second = individual[i][0]
                if first != second:
                    pair = False
            if pair:
                score = score + 100
            else:
                score = score - 100
    return score


def individual_fitness(individual, target, possible_chords):
    """
    This function is used to get the fitness score of an individual.
    The fitness score is based on three criteria
    1- The similarity of each chord in the individual to the average note played
          in the same quarter of the original melody.
    2- The existence of each chord of the individual in the possible chords
          we can compose out of the original melody key.
    3- The similarity of each chord in the individual to the previous two chords
          in the individual

    :param individual: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes
    :param target: list[float]: the average notes played in each quarter of a bar in the original melody
    :param possible_chords: list[char]: the possible notes to compose a chord from in the original melody's key
    :return: float: the overall fitness of the individual
    """
    score = 0
    score = score + similarity_to_original_melody(individual, target)
    score = score + chord_exists(individual, possible_chords)
    score = score + redundant_chords(individual)
    return score


def selection(population, target, possible_chords):
    """
    This function is the selection phase of the evolutionary algorithm
    The selection method: Tournament
    We order the population in a random order, then each two consecutive individuals face each other in a match
    the winner of the match is decided based on the individual's fitness scores
    we do only one round of the tournament to cut the population size by half then we return the winners

    :param population: list[list[int,int,int]]: a population consisting individuals consisting of chords consisting of
                        three notes
    :param target: list[float]: the average notes played in each quarter of a bar in the original melody
    :param possible_chords: list[char]: the possible notes to compose a chord from in the original melody's key
    :return: list[list[int,int,int]]: the individuals that won in the tournament
    """
    tournament_bracket = np.random.permutation(population)
    tournament_winners = []
    for contestantID in range(len(tournament_bracket)):
        if contestantID % 2:
            continue
        if individual_fitness(tournament_bracket[contestantID], target, possible_chords) > individual_fitness(
                tournament_bracket[contestantID + 1], target, possible_chords):
            tournament_winners.append(tournament_bracket[contestantID])
        else:
            tournament_winners.append(tournament_bracket[contestantID + 1])
    return tournament_winners


def crossover(population):
    """
    This function is the crossover and mutation phases of the evolutionary algorithm
    The crossover method: n-point crossover
    We order the population in a random order, then each two consecutive individuals are considered as parents
    that will mate together and produce two new children
    We do that by iterating through the chords of the parents and do the following based on a 50% probability:
    1- Child1 gets the chord from Parent1, Child2 gets the chord from Parent2
    2- Child1 gets the chord from Parent2, Child2 gets the chord from Parent1

    Each child is the exact opposite of the other.

    Then we mutate the children by calling the function mutation, and we pass to it the child.
    Which will return the mutated child.

    After that we add the mutated children and the parents to the final output

    :param population: list[list[int,int,int]]: a population consisting individuals consisting of chords consisting of
                        three notes. that represents the winners of the selection process
    :return: list[list[int,int,int]]: the new population consisting of the winners of the tournament bracket and the
                                         mutated children
    """
    parents = np.random.permutation(population)
    new_population = []
    for parent in range(len(parents)):
        if parent % 2:
            continue
        new_population.append(parents[parent])
        new_population.append(parents[parent + 1])
        new_child1 = []
        new_child2 = []
        for i in range(len(parents[parent])):
            probability_of_crossover = random.uniform(0, 1)
            if probability_of_crossover >= 0.5:
                new_child1.append(parents[parent][i])
                new_child2.append(parents[parent + 1][i])
            else:
                new_child1.append(parents[parent + 1][i])
                new_child2.append(parents[parent][i])
        new_population.append(mutation(new_child1))
        new_population.append(mutation(new_child2))
    return new_population


def mutation(individual):
    """
    This function is the mutation phase of the evolutionary algorithm
    The mutation method: replacement of a chromosome with a random new one

    We iterate through the chords of the child and with a 5% probability we replace the current chord
    with a new random chord

    Then we return the mutated child

    :param individual: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes.
                        that represents the child we want to mutate
    :return: list[int,int,int]: the individual which has several chords, each chord consisting of 3 notes
                that represents the mutated child
    """
    for chord in range(len(individual)):
        probability_of_mutation = random.uniform(0, 1)
        if probability_of_mutation < 0.05:
            individual[chord] = random.choice(
                [
                    major_triad(random.randint(0, 110)),
                    minor_triad(random.randint(0, 110)),
                    first_inverted_major(random.randint(0, 110)),
                    first_inverted_minor(random.randint(0, 110)),
                    second_inverted_major(random.randint(0, 110)),
                    second_inverted_minor(random.randint(0, 110)),
                    sus2(random.randint(0, 110)),
                    sus4(random.randint(0, 110)),
                    diminished(random.randint(0, 110)),
                    rest()
                ]
            )
    return individual


def analyze_generation(generation, population, average, possible_chords):
    """
    This function is used to analyze a generation in the evolution
    It outputs:
    1- the generation number
    2- the maximum fitness in the population
    3- the minimum fitness in the population

    :param generation: integer: the current generation
    :param population: list[list[int,int,int]]: a population consisting individuals consisting of chords consisting of three notes.
    :param average: list[float]: the average notes played in each quarter of a bar in the original melody
    :param possible_chords: list[char]: the possible notes to compose a chord from in the original melody's key
    :return:
    """
    mx = 0
    mn = 10000000
    for individual in population:
        mx = max(mx, individual_fitness(individual, average, possible_chords))
        mn = min(mn, individual_fitness(individual, average, possible_chords))
    print("Gen: ", generation)
    print("MAX: ", mx)
    print("min: ", mn)
    return


def get_best_individual(population, average, possible_chords):
    """
    This function is used to get the best individual in the population based on the fitness scores
    by calculating the fitness score for each individual and seeing if it is better than
    the best individual we came across so far

    :param population: list[list[int,int,int]]: a population consisting individuals consisting of chords consisting
                        of three notes.
    :param average: list[float]: the average notes played in each quarter of a bar in the original melody
    :param possible_chords: list[char]: the possible notes to compose a chord from in the original melody's key
    :return: list[int,int,int]: the best individual in the population
    """
    best_individual = []
    mx = 0
    for individual in population:
        if individual_fitness(individual, average, possible_chords) > mx:
            mx = individual_fitness(individual, average, possible_chords)
            best_individual = individual
    return best_individual


def get_possible_chords(input_file_name):
    """
    This function is used to get a list of notes that we can compose valid chords from
    by getting the key of the input and based on it, we get the list of notes from the
    major keys or the minor keys, which consist of the list of notes for each possible key.

    we get the key of the original melody using the feature converter.parse from the library: music21

    :param input_file_name: string: the input midi file name
    :return: list[char]: the list consisting of the notes that we can compose valid chords from based on the key of the
                            original melody
    """
    possible_chords = []

    major_keys = [
        ['C', ['C', 'D', 'E', 'F', 'G', 'A', 'B']],
        ['C#', ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']],
        ['D', ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']],
        ['D#', ['D#', 'F', 'G', 'G#', 'A#', 'C', 'D']],
        ['E', ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']],
        ['F', ['F', 'G', 'A', 'A#', 'C', 'D', 'E']],
        ['F#', ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']],
        ['G', ['G', 'A', 'B', 'C', 'D', 'E', 'F#']],
        ['G#', ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'F#']],
        ['A', ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']],
        ['A#', ['A#', 'C', 'D', 'D#', 'F', 'G', 'A']],
        ['B', ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']]
    ]

    minor_keys = [
        ['C', ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#']],
        ['C#', ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B']],
        ['D', ['D', 'E', 'F', 'G', 'A', 'A#', 'C']],
        ['D#', ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#']],
        ['E', ['E', 'F#', 'G', 'A', 'B', 'C', 'D']],
        ['F', ['F', 'G', 'G#', 'A#', 'C', 'C#', 'D#']],
        ['F#', ['F#', 'G', 'A', 'B', 'C#', 'D', 'E']],
        ['G', ['G', 'A', 'A#', 'C', 'D', 'D#', 'F']],
        ['G#', ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#']],
        ['A', ['A', 'B', 'C', 'D', 'E', 'F', 'G']],
        ['A#', ['A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#']],
        ['B', ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']]
    ]

    input_song = parse(input_file_name)
    key = input_song.analyze('key')
    root_note = str(key).split()[0].capitalize()
    if key.type == 'minor':
        for keys in minor_keys:
            if keys[0] == root_note:
                possible_chords = keys[1]
    else:
        for keys in major_keys:
            if keys[0] == root_note:
                possible_chords = keys[1]
    return possible_chords


def write_output(input_mid, best_individual, output_file_name):
    """
    This function is used to create the output file.
    we do that by using the features in the library: mido
    first: we make a new output Midifile, and we append to it the tracks of the input file
    second: we append each chord of the best individual using the following method:
                  1) add one mido.Message with:
                                               a) note.type = "note_on"
                                               b) the time = rest_time which is the time spent without playing anything
                                               c) note = tonic of the chord
                  2) add one mido.Message with:
                                               a) note.type = "note_on"
                                               b) the time = 0
                                               c) note = mediant of the chord
                  3) add one mido.Message with:
                                               a) note.type = "note_on"
                                               b) the time = 0
                                               c) note = dominant of the chord
                  4) add one mido.Message with:
                                               a) note.type = "note_off"
                                               b) the time = 384 which is the time of a quarter
                                               c) note = tonic of the chord
                  5) add one mido.Message with:
                                               a) note.type = "note_off"
                                               b) the time = 0
                                               c) note = mediant of the chord
                  6) add one mido.Message with:
                                               a) note.type = "note_off"
                                               b) the time = 0
                                               c) note = dominant of the chord
    third: we append the track to the output midifile.
    fourth: we save the output midifile using mido.Midifile.save(output_file_name)

    :param input_mid: mido.Midifile: that contains the midi file we want to parse
    :param best_individual: list[int,int,int]: the best individual after the evolution
    :param output_file_name: string: the name of the file we want to save the output to
    :return:
    """
    output_mid = MidiFile()
    output_mid.tracks.append(input_mid.tracks[0])
    output_mid.tracks.append(input_mid.tracks[1])

    generated_track = MidiTrack()
    generated_track.append(input_mid.tracks[1][0])
    rest_time = 0
    for x in best_individual:
        tonic = x[0]
        mediant = x[1]
        dominant = x[2]
        if tonic == 0:
            rest_time = rest_time + quarter_time
            continue
        generated_track.append(Message("note_on", channel=0, note=tonic, velocity=50, time=rest_time))
        if rest_time != 0:
            rest_time = 0
        generated_track.append(Message("note_on", channel=0, note=mediant, velocity=50, time=0))
        generated_track.append(Message("note_on", channel=0, note=dominant, velocity=50, time=0))
        generated_track.append(Message("note_off", channel=0, note=tonic, velocity=0, time=quarter_time))
        generated_track.append(Message("note_off", channel=0, note=mediant, velocity=0, time=0))
        generated_track.append(Message("note_off", channel=0, note=dominant, velocity=0, time=0))

    generated_track.append(input_mid.tracks[1][len(input_mid.tracks[1]) - 1])

    output_mid.tracks.append(generated_track)
    output_mid.ticks_per_beat = input_mid.ticks_per_beat

    output_mid.save(output_file_name)
    return


def main(input_file_name, output_file_name):
    """
    This is the main function
    it consists of the error handling regarding finding the input file,
    and it consists of the main evolution process and the function calls

    :param input_file_name: string: the input midi file name
    :param output_file_name: string: the output midi file name
    :return:
    """

    input_mid = MidiFile(input_file_name, clip=True)

    number_of_generations = 5000

    size_of_population = 1024

    original_melody = parse_input(input_mid)

    possible_chords = get_possible_chords(input_file_name)

    average = average_notes(original_melody)

    population = create_population(size_of_population, len(average))
    for i in range(number_of_generations):
        selected_population = selection(population, average, possible_chords)
        new_population = crossover(selected_population)
        population = new_population
        if i % 100 == 0:
            analyze_generation(i, population, average, possible_chords)

    best_individual = get_best_individual(population, average, possible_chords)

    write_output(input_mid, best_individual, output_file_name)

    return


if __name__ == '__main__':
    main("input1.mid", "MosabMohamedOutput1.mid")
    main("input2.mid", "MosabMohamedOutput2.mid")
    main("input3.mid", "MosabMohamedOutput3.mid")
