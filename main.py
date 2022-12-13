from Pyro4 import expose
from os import stat
from heapq import merge

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        processed_arr = self.read_input()

        step = len(processed_arr) / len(self.workers)
        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(processed_arr[i * step:i * step + step]))
        reduced = self.myreduce(mapped)
        self.write_output(reduced)


    @staticmethod
    @expose
    def myreduce(mapped):
      arr_num = len(mapped)
      res = mapped[0].value
      for i in range(1,arr_num):
          res = list(merge(res,list(mapped[i].value)))
      return res


    @staticmethod
    @expose
    def mymap(array):
        swapped = False
        for n in range(len(array) - 1, 0, -1):
            for i in range(n):
                if array[i] > array[i + 1]:
                    swapped = True
                    array[i], array[i + 1] = array[i + 1], array[i]
            if not swapped:
                return
        return array


    def read_input(self):
        f = open(self.input_file_name, 'r')

        array = []
        arr_line = f.readline().split(' ')
        for element in arr_line:
            if element != '':
                array.append(int(element))
        f.close()
        return array


    def write_output(self, output):
        f = open(self.output_file_name, 'a')
        f.write(str(output))
        f.write('\n')
        f.close()

