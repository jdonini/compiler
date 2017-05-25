import os
import sys
import datetime

class Utils(object):
    """ """
    def __init__(self, arg):
        self.arg = arg

    def find_files(path_files_test):
        archives = []
        number_archives = ''
        answer = False
        count = 1

        for base, dirs, files in os.walk(path_files_test):
            archives.append(files)

            for file in files:
                print(str(count)+". "+file)
                count += 1

            if answer is False:
                number_archives = input('\nNúmero do Teste: ')
                for file in files:
                    if file == files[int(number_archives)-1]:
                        break
                print("Você escolheu \"%s\" \n" % files[int(number_archives)-1])

                return files[int(number_archives)-1]


    def find_files_test(archive, path_files_test):
        test = path_files_test + archive
        test_archive = open(test, "r")
        input_string = test_archive.read()
        test_archive.close()
        return input_string


    def save_archives_test(archive, path_files_result):
        result_directory = path_files_result
        time = datetime.datetime.now()
        result = result_directory + archive + \
            "__" + ("%s-%s-%s" % (time.day, time.month, time.year)) + \
            "__" + ("%s:%s:%s" % (time.hour, time.minute, time.second)) + ".txt"
        return result
