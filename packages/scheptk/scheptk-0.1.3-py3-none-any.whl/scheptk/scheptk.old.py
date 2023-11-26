from abc import ABC, abstractmethod #abstract classes
import sys # to stop the execution (funcion exit() )
import os # to implement deletion of files
import operator # for sorted functions
import matplotlib.pyplot as plt
from random import randint # random solutions

from scheptk.util import random_sequence, read_tag, find_index_min, print_tag, sorted_index_asc, sorted_value_asc, sorted_value_desc, write_tag


class Task:

    def __init__(self, job, machine, st, ct):
        self.job = job
        self.machine = machine
        self.st = st
        self.ct = ct


class Schedule():

    def __init__(self, filename=None):

        # list of tasks in the schedule
        self.task_list = []
        # job order (order to indicate which is each job in the schedule)
        self.job_order = []

        if(filename != None):
            # load the tag with the job order
            self.job_order = read_tag(filename,'JOB_ORDER')
            # load the tag with the tasks
            tasks = read_tag(filename,'SCHEDULE_DATA')
            for j, tasks_job in enumerate(tasks):
                index_task_in_job = 0
                while(index_task_in_job < len(tasks_job)):
                    self.add_task(Task(self.job_order[j], tasks_job[index_task_in_job], tasks_job[index_task_in_job + 1], tasks_job[index_task_in_job + 1] + tasks_job[index_task_in_job + 2]))
                    index_task_in_job += 3

    def add_task(self, task):

        # add the task to the list
        self.task_list.append(task)

        # add the job to the job order (in case it is a new job)
        if( self.job_order.count(task.job) == 0):
            self.job_order.append(task.job)



    # save the schedule in a file
    def save(self,filename):

        # compute number of machines
        machines = set([task.machine for task in self.task_list])
        
        # delete existing schedule
        if(os.path.exists(filename)):
           os.remove(filename)

        # only the jobs that have to be displayed (those in the sequence)
        write_tag('JOBS', len(self.job_order), filename)
        write_tag('MACHINES',len(machines), filename)        

        # schedule data matrix
        tag_value = ''
        # for all jobs write the corresponding task (ordered jobs)       
        for j, job in enumerate(self.job_order):
            sorted_tasks_in_job = sorted([[task.machine,task.st, task.ct] for task in self.task_list if task.job == job ], key=operator.itemgetter(1), reverse=False)
            for index,task in enumerate(sorted_tasks_in_job):
                tag_value = tag_value + '{},{},{}'.format(task[0], task[1], task[2] - task[1])
                if(index ==len(sorted_tasks_in_job)-1):
                    if( j!= len(self.job_order)-1):
                        tag_value = tag_value + ';'
                else:
                    tag_value = tag_value + ','
        write_tag('SCHEDULE_DATA', tag_value, filename)
        write_tag('JOB_ORDER',self.job_order, filename)


    # print a basic gantt with the schedule given. Optionally, it saves the gantt in a png image
    def print(self, filename=None):
        
        # parameters of the graphic
        tick_starting_at = 10
        tick_separation = 20
        task_height = 8
        font_height = 1

        # palette of light colors
        colors = ['red','lime','deepskyblue','bisque','mintcream','royalblue','sandybrown','palegreen','pink','violet','cyan','darkseagreen','gold']

        # compute number of machines
        machines = set([task.machine for task in self.task_list])

        # create gantt
        figure, gantt = plt.subplots()    
        
        # limits (makespan and depending on the number of machines)
        gantt.set_xlim(0,max([task.ct for task in self.task_list]))
        gantt.set_ylim(0,len(machines) * tick_separation + tick_starting_at)
 
        # labels
        gantt.set_xlabel('Time')
        gantt.set_ylabel('Machines')

        # ticks labels (y)
        gantt.set_yticks([tick_starting_at + tick_separation *i + task_height/2 for i in range(len(machines))])
        gantt.set_yticklabels(['M'+str(i) for i in range(len(machines)-1,-1,-1)])

        # populate the gantt
        for job in self.job_order:

            # get the tasks associated to the job
            tasks_job = [[[(task.st, task.ct-task.st)],(tick_starting_at + tick_separation * (len(machines) - task.machine - 1), task_height)] for task in self.task_list if task.job == job]

            # prints the rectangle and the text
            for task in tasks_job:
                gantt.broken_barh(task[0],task[1],facecolors=colors[job % len(colors)], edgecolors='black', label = 'J' + str(job))
                gantt.text(task[0][0][0] + task[0][0][1]/2, task[1][0] + task_height/2 - font_height,'J' + str(job))

        # optionally, the gantt is printed in hi-res
        if(filename != None):
            figure.savefig(filename, dpi=600, facecolor='w')



class Model(ABC):
 
    # basic data, common to all layouts
    def __init__(self):
        self.jobs = 0 
        self.pt = []
        self.dd = []
        self.w = [] # weigths
        self.r = [] # release dates
   
 
    @abstractmethod
    def ct(self, sequence):
        pass
  
    # concrete method: it returns the completion time of each job in the sequence 
    # it is a bit tricky so it can support different codifications of the solutions in each layout
    def Cj(instance, seq):

        ct, job_order = instance.ct(seq)
        # it is done with len(ct[0]) in order to support JobShop and OpenShop, because len(seq) is different than the number of jobs in ct
        # and it is done with len(ct) instead of machines to support SingleMachine
        Cj = [max([ct[i][j] for i in range(len(ct))]) for j in range(len(job_order))]
    
        return Cj


    # concrete method makespan
    def Cmax(self, sequence):
        return max(self.Cj(sequence))

    #  earliness of all jobs
    def Ej(self, sequence):
         if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")        
         return [ max(self.dd[sequence[index]] - item,0) for index,item in enumerate(self.Cj(sequence))]

    # max earliness
    def Emax(self, sequence):    
         return max(self.Lj(sequence)) 

   #  flowtime de cada uno de los trabajos
    def Fj(self, sequence):
        return [item - self.r[sequence[index]] for index,item in enumerate(self.Cj(sequence))]         

   # max flowtime
    def Fmax(self, sequence):
        return max( self.Fj(sequence))
        
    # lateness of all jobs in the sequence
    def Lj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")        
        return [item - self.dd[sequence[index]] for index,item in enumerate(self.Cj(sequence))]

    # max lateness
    def Lmax(self, sequence):
        return max(self.Lj(sequence))

    # tardiness of all jobs
    def Tj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return [ max(item - self.dd[sequence[index]],0) for index,item in enumerate(self.Cj(sequence))]

    # max tardiness
    def Tmax(self, sequence):
        return max(self.Tj(sequence))

    # sum of completion tme
    def SumCj(self, sequence):
        return sum(self.Cj(sequence))

    # sum earliness
    def SumEj(self, sequence):
        return sum(self.Ej(sequence))

   # sum flowtime
    def SumFj(self, sequence):
        return sum(self.Fj(sequence))

    # sum lateness
    def SumLj(self, sequence):
        return sum( self.Lj(sequence))

    # sum tardiness
    def SumTj(self, sequence):
        return sum( self.Tj(sequence))           

    # sum of tardy jobs
    def SumUj(self, sequence):
        return sum( self.Uj(sequence))

    # weighted makespan
    def WjCmax(self, sequence):
        return max([item * self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])

    # weighted max earliness
    def WjEmax(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")        
        return max([ (max(self.dd[sequence[index]] - item,0) * self.w[sequence[index]]) for index,item in enumerate(self.Cj(sequence))])

   # weighted max flowtime
    def WjFmax(self, sequence):
        return max([(item - self.r[sequence[index]])* self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])
        
    # weighted max lateness
    def WjLmax(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return max([ (item - self.dd[sequence[index]])*self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])

    # weighted max tardiness
    def WjTmax(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return max([ (max(item - self.dd[sequence[index]],0) * self.w[sequence[index]]) for index,item in enumerate(self.Cj(sequence))])
        
    # weighted sum of completion times
    def SumWjCj(self, sequence):
        return sum([item * self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])

    # weighted sum of earliness
    def SumWjEj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")        
        return sum([ (max(self.dd[sequence[index]] - item,0) * self.w[sequence[index]]) for index,item in enumerate(self.Cj(sequence))])

    # weighted sum of flowtime
    def WjFmax(self, sequence):
        return sum([(item - self.r[sequence[index]])* self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])
   
    # weighted sum of lateness
    def SumWjLj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return sum([ (item - self.dd[sequence[index]])*self.w[sequence[index]] for index,item in enumerate(self.Cj(sequence))])

    # weighted sum of tardiness
    def SumWjTj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return sum([ (max(item - self.dd[sequence[index]],0) * self.w[sequence[index]]) for index,item in enumerate(self.Cj(sequence))])

    # weighted sum of tardy jobs
    def SumWjUj(self, sequence):
        if(self.dd == -1):
            print("The instance does not have due dates and due-date related objective cannot be computed.")
        return sum([1 if (item - self.dd[sequence[index]]) > 0 else 0 for index,item in enumerate(self.Cj(sequence))])

    # vector of tardy jobs: 1 if the job is tardy, 0 otherwise
    def Uj(self, sequence):
        return [1 if t >0 else 0 for t in self.Tj(sequence)]


    # other methods to check data that are implemented in all children
    def check_duedates(self, filename):
        # due dates (if not,  -1 is assumed)
        self.dd = read_tag(filename, "DD")
        if(self.dd ==-1):
            print("No due dates specified for the jobs. All due dates assummed to be infinite. No due-date related objectives can be computed.")           
        else:
            # if the type is an int (single number), it is transformed into a list
            if( type(self.dd) == int):
                self.dd = [self.dd]

            if(len(self.dd)!= self.jobs):
                print("Number of due dates given in tag DD is different that the number of jobs (JOBS={}, length of DD={}). The program cannot continue.".format(self.jobs, len(self.dd)))     
                sys.exit()              
            else:
                print_tag("DD", self.dd)

    def check_weights(self, filename):
        # checking weights, if not all are assumed to be 1.0
        self.w = read_tag(filename, "W")
        if(self.w ==-1):
            self.w = [1.0 for i in range(self.jobs)]
            print("No weights specified for the jobs. All weights set to 1.0.") 
        else:
            # if the type is an int (single number), it is transformed into a list
            if( type(self.w) == int):
                self.w = [self.w]

            if(len(self.w) != self.jobs):
                print("Number of weights given in tag W is different that the number of jobs (JOBS={}, length of W={}). The program cannot continue.".format(self.jobs, len(self.w)))
                sys.exit()
            else:
                print_tag("W", self.w)

    def check_releasedates(self, filename):
        self.r = read_tag(filename,"R")
        if(self.r==-1):
            self.r = [0 for i in range(self.jobs)]
            print("No release dates specified for the jobs. All release dates set to zero.")   
        else:
            # if the type is an int (single number), it is transformed into a list
            if( type(self.r) == int):
                self.r = [self.r]

            if(len(self.r)!= self.jobs):
                 print("Number of release dates given in tag R is different that the number of jobs (JOBS={}, length of R={}). The program cannot continue.".format(self.jobs, len(self.r)))
                 sys.exit()               
            else:
                print_tag("R", self.r)

    #  method to create a schedule. This method is implemented by the children clasess
    # The method is a bit tricky to treat the case of a single machine and parallel machines (which is not ideal for a parent class :-( )),
    #  as in this case it is not usual to use a matrix for the processing times
    def create_schedule(self, solution):

        # tricky part to treat properly the single machine and the identical machine case
        # in the processing times are a list 
        if not isinstance(self.pt[0],list):
            # it can be parallel machines or single machine
            if not hasattr(self, 'machines'):
                # single machine
                pt = [self.pt]
            else:
                # parallel machines
                pt = [self.pt for i in range(self.machines)]
        else:
            # in the rest of the cases, it is already a list of lists
            pt = self.pt          

        gantt = Schedule()
        ct, job_order = self.ct(solution)
        for j, job in enumerate(job_order):
            for mach in range(len(ct)):
                # if ct not zero (some ct may be zero, check ParallelMachine)
                if(ct[mach][j]!= 0):
                    # add the task    
                    gantt.add_task(Task(job, mach, ct[mach][j] - pt[mach][job], ct[mach][j]))
                
        return gantt
                    


    # method to write a schedule in a file
    def write_schedule(self, solution, filename):
        gantt = self.create_schedule(solution)
        gantt.save(filename)

    # method to print (console) a schedule. Optionally it can be printed into a png file
    def print_schedule(self, solution, filename=None):
        gantt = self.create_schedule(solution)
        gantt.print(filename)



# class to implement the single machine layout
class SingleMachine(Model):
     
    def __init__(self, filename):

        print("----- Reading SingleMachine instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        
        # processing times (mandatory data)
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.jobs ):
                print("Number of processing times does not match the number of jobs (JOBS={}, length of PT={}). The program cannot continue".format(self.jobs, len(self.pt)) )
                sys.exit()                
            else:
                print_tag("PT", self.pt)
        
        # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)
        
        print("----- end of SingleMachine instance data from file " + filename + " -------")
        

    # implementation of the computation of the completion times
    def ct(self,sequence):
        completion_time = []
        completion_time.append(self.r[sequence[0]] + self.pt[sequence[0]])
        for i in range(1,len(sequence)):
            completion_time.append(max(completion_time[i-1],self.r[sequence[i]]) + self.pt[sequence[i]])
        return [completion_time], sequence

    # implementation of random_solution()
    def random_solution(self):
        return random_sequence(self.jobs)


      

# class to implement the flowshop layout
class FlowShop(Model):
 
    def __init__(self, filename):

        # initializing additional data (not basic)
        self.machines = 0

        # starting reading
        print("----- Reading FlowShop instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        # machines (another mandatory data)
        self.machines = read_tag(filename, "MACHINES")
        if(self.machines ==-1):
            print("No machines specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("MACHINES", self.machines)

        # processing times (mandatory data, machines in rows, jobs in cols)
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.machines ):
                print("Number of processing times does not match the number of machines (MACHINES={}, length of PT={}). The program cannot continue".format(self.machines, len(self.pt)) )
                sys.exit()
            else:
                for i in range(self.machines):
                    if(len(self.pt[i])!= self.jobs):
                        print("Number of processing times does not match the number of jobs for machine {} (JOBS={}, length of col={}). The program cannot continue".format(i, self.jobs, len(self.pt[i])) )
                        sys.exit()
                print_tag("PT", self.pt)           
        
         # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)

        print("----- end of FlowShop instance data from file " + filename + " -------")    

    # implementation of random_solution()
    def random_solution(self):
        return random_sequence(self.jobs)


    # implementation of the completion times of each job on each machine for FlowShop
    def ct(self,sequence):
         # initializing the completion times
        completion_time = [[0 for j in range(len(sequence))] for i in range(self.machines)]
        # first job in first machine
        completion_time[0][0] = self.r[sequence[0]] + self.pt[0][sequence[0]] 
        # first job in all machines
        for i in range(1,self.machines):
            completion_time[i][0] = completion_time[i-1][0] + self.pt[i][sequence[0]]
        # rest of jobs in first machine
        for j in range(1, len(sequence)):
            completion_time[0][j] =max(completion_time[0][j-1], self.r[sequence[j]]) + self.pt[0][sequence[j]]
        # rest of jobs in rest of machines
        for i in range(1, self.machines):
            for j in range(1, len(sequence)):
                completion_time[i][j] = max(completion_time[i-1][j], completion_time[i][j-1]) + self.pt[i][sequence[j]]  
        return completion_time, sequence     



# identical parallel machines
class ParallelMachines(Model):
   def __init__(self, filename):

        # initializing additional data (not basic)
        self.machines = 0

        # starting reading
        print("----- Reading ParallelMachines instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        # machines (another mandatory data)
        self.machines = read_tag(filename, "MACHINES")
        if(self.machines ==-1):
            print("No machines specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("MACHINES", self.machines)

        # processing times (a vector, one pt for jobs). Mandatory
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.jobs ):
                print("Number of processing times does not match the number of jobs (JOBS={}, length of PT={}). The program cannot continue".format(self.jobs, len(self.pt)) )
                sys.exit()                
            else:
                print_tag("PT", self.pt)

        # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)

        print("----- end of ParallelMachines instance data from file " + filename + " -------")    
  

    # implementation of completion times for parallel machines (ECT rule)
    # ties are broken with the lowest index
   def ct(self, sequence):

        # initializing completion times in the machines to zero
        ct_machines = [0 for i in range(self.machines)]
        ct = [[0 for j in range(len(sequence))] for i in range(self.machines)]
        
        # assign all jobs
        for j in range(len(sequence)):
            # assign the job to the machine finishing first
            index_machine = find_index_min(ct_machines)
            # increases the completion time of the corresponding machine (and sets the completion time of the job)
            ct_machines[index_machine] = max(ct_machines[index_machine], self.r[sequence[j]]) + self.pt[sequence[j]]
            ct[index_machine][j] = ct_machines[index_machine]
    
        return ct, sequence        


    # implementation of random_solution()
   def random_solution(self):
        return random_sequence(self.jobs)


     





class UnrelatedMachines(Model):
   def __init__(self, filename):

        # initializing additional data (not basic)
        self.machines = 0

        # starting reading
        print("----- Reading UnrelatedMachines instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        # machines (another mandatory data)
        self.machines = read_tag(filename, "MACHINES")
        if(self.machines ==-1):
            print("No machines specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("MACHINES", self.machines)

        # processing times (mandatory data, machines in rows, jobs in cols)
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.machines ):
                print("Number of processing times does not match the number of machines (MACHINES={}, length of PT={}). The program cannot continue".format(self.machines, len(self.pt)) )
                sys.exit()
            else:
                for i in range(self.machines):
                    if(len(self.pt[i])!= self.jobs):
                        print("Number of processing times does not match the number of jobs for machine {} (JOBS={}, length of col={}). The program cannot continue".format(i, self.jobs, len(self.pt[i])) )
                        sys.exit()
                print_tag("PT", self.pt)     

        # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)   
  

    # implementation of completion times for unrelated parallel machines (ECT rule)
    # ties are broken with the lowest index
   def ct(self, sequence):

        # initializing completion times in the machines to zero
        ct_machines = [0 for i in range(self.machines)]
        ct = [[0 for j in range(len(sequence))] for i in range(self.machines)]

        # assign all jobs
        for j in range(len(sequence)):
            # construct what completion times would be if the job is assigned to each machine
            next_ct = [max(ct_machines[i],self.r[sequence[j]]) + self.pt[i][sequence[j]] for i in range(self.machines)]
            # assign the job to the machine finishing first
            index_machine = find_index_min(next_ct)
            # increases the completion time of the corresponding machine (and sets the completion time of the job)
            ct_machines[index_machine] = max(ct_machines[index_machine], self.r[sequence[j]]) + self.pt[index_machine][sequence[j]]
            ct[index_machine][j] = ct_machines[index_machine]
    
        return ct, sequence

   # implementation of random_solution()
   def random_solution(self):
        return random_sequence(self.jobs)


 


class JobShop(Model):
     def __init__(self, filename):

        # initializing additional data (not basic)
        self.machines = 0
        self.rt = []

        # starting reading
        print("----- Reading JobShop instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        # machines (another mandatory data)
        self.machines = read_tag(filename, "MACHINES")
        if(self.machines ==-1):
            print("No machines specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("MACHINES", self.machines)

        # processing times (mandatory data, machines in rows, jobs in cols)
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.machines ):
                print("Number of processing times does not match the number of machines (MACHINES={}, length of PT={}). The program cannot continue".format(self.machines, len(self.pt)) )
                sys.exit()
            else:
                for i in range(self.machines):
                    if(len(self.pt[i])!= self.jobs):
                        print("Number of processing times does not match the number of jobs for machine {} (JOBS={}, length of col={}). The program cannot continue".format(i, self.jobs, len(self.pt[i])) )
                        sys.exit()
                print_tag("PT", self.pt)           
        
        # routing matrix times (mandatory data, machines in rows, jobs in cols)
        self.rt = read_tag(filename,"RT")
        if(self.rt ==-1):
            print("No routing specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.rt) != self.jobs ):
                print("Number of routes does not match the number of jobs (JOBS={}, length of RT={}). The program cannot continue".format(self.jobs, len(self.rt)) )
                sys.exit()
            else:
                for j in range(self.jobs):
                    if(len(self.rt[j])!= self.machines):
                        print("Number of visiting stations does not match the number of machines for job {} (MACHINES={}, length of col={}). The program cannot continue".format(j, self.machines, len(self.rt[j])) )
                        sys.exit()
                print_tag("RT", self.rt)           

        # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)

        # release dates (if not, 0 is assumed)
        self.r = read_tag(filename,"R")
        if(self.r==-1):
            self.r = [0 for i in range(self.jobs)]
            print("No release dates specified for the jobs. All release dates set to zero.")    
        else:
            print_tag("R", self.r)

        print("----- end of JobShop instance data from file " + filename + " -------")    


     def ct(self, solution):
         
       # get the jobs involved in the solution in the order they are processed
       jobs_involved = list(set(solution))

       # completion times of jobs and machines
       ct_jobs = [self.r[jobs_involved[j]] for j in range(len(jobs_involved))]
       ct_machines = [0 for i in range(self.machines)]  

       # completion time of each job on each machine
       ct = [[0 for j in range(len(jobs_involved))] for i in range(self.machines)]

       # number of operations completed by each job (initially zero)
       n_ops_jobs = [0 for j in range(len(jobs_involved))]

       for job in solution:

           # determine the corresponding machine
           machine = self.rt[job][n_ops_jobs[jobs_involved.index(job)]]

           # compute completion time
           curr_completion_time = max(ct_jobs[jobs_involved.index(job)], ct_machines[machine]) + self.pt[machine][job]

           # update completion times
           ct_jobs[jobs_involved.index(job)] = curr_completion_time
           ct_machines[machine] = curr_completion_time
           #print("index={}, machine={}".format(index,machine))
           ct[machine][jobs_involved.index(job)] = curr_completion_time

           # update number of operations for the job
           n_ops_jobs[jobs_involved.index(job)] += 1

       return ct, jobs_involved

   
    
     # implementation of a random solution of the instance
     def random_solution(self):
        solution = []
        curr_op = 0
        total_ops = self.jobs * self.machines
        pending_ops = [self.machines for j in range(self.jobs)]
        while(curr_op < total_ops):
            job = randint(0,self.jobs-1)
            if(pending_ops[job] > 0):
                solution.append(job)
                pending_ops[job] = pending_ops[job]-1
                curr_op = curr_op + 1
        return solution

 


class OpenShop(Model):

    def __init__(self, filename):

        # initializing additional data (not basic)
        self.machines = 0

        # starting reading
        print("----- Reading OpenShop instance data from file " + filename + " -------")
        # jobs (mandatory data)
        self.jobs = read_tag(filename,"JOBS")
        # if jobs = -1 the program cannot continue
        if(self.jobs ==-1):
            print("No jobs specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("JOBS", self.jobs)
        # machines (another mandatory data)
        self.machines = read_tag(filename, "MACHINES")
        if(self.machines ==-1):
            print("No machines specified. The program cannot continue.")
            sys.exit()
        else:
            print_tag("MACHINES", self.machines)

        # processing times (mandatory data, machines in rows, jobs in cols)
        self.pt = read_tag(filename,"PT")
        if(self.pt ==-1):
            print("No processing times specified. The program cannot continue.")
            sys.exit()
        else:
            if(len(self.pt) != self.machines ):
                print("Number of processing times does not match the number of machines (MACHINES={}, length of PT={}). The program cannot continue".format(self.machines, len(self.pt)) )
                sys.exit()
            else:
                for i in range(self.machines):
                    if(len(self.pt[i])!= self.jobs):
                        print("Number of processing times does not match the number of jobs for machine {} (JOBS={}, length of col={}). The program cannot continue".format(i, self.jobs, len(self.pt[i])) )
                        sys.exit()
                print_tag("PT", self.pt)           
        
        # weights (if not, default weights)
        self.check_weights(filename)

        # due dates (if not,  -1 is assumed)
        self.check_duedates(filename)

        # release dates (if not, 0 is assumed)
        self.check_releasedates(filename)

        print("----- end of OpenShop instance data from file " + filename + " -------")    

    # implementation of random_solution()
    def random_solution(self):
        return random_sequence(self.jobs * self.machines)

    # implementation of the completion times of each job on each machine for OpenShop
    # it has to be a full sequence
    def ct(self, sequence):
         
       # completion times of jobs and machines
       ct_jobs = [self.r[j] for j in range(self.jobs)]
       ct_machines = [0 for i in range(self.machines)]  

       # completion time of each job on each machine
       ct = [[0 for j in range(self.jobs)] for i in range(self.machines)]

       for job in sequence:

           # obtain decoded_job
           decoded_job = job % self.jobs
           
           # obtain decoded machine
           decoded_machine = int((job - decoded_job) / self.jobs)

           # compute completion time
           curr_completion_time = max(ct_jobs[decoded_job], ct_machines[decoded_machine]) + self.pt[decoded_machine][decoded_job]
           ct_jobs[decoded_job]= curr_completion_time
           ct_machines[decoded_machine] = curr_completion_time

           ct[decoded_machine][decoded_job] = curr_completion_time

       return ct, ct_jobs
   

   


