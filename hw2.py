
"""
William Jack
Constraint Satisfaction
"""

"""
A
conference has a sign-in desk where attendees check in.  Two students must man the
sign-in desk at all times, in hourlong shifts.  Each student is volunteering because if she does two volunteer
shifts, her conference registration fee is waived.  However, each student is
only available for a few hours, since she has talks she wants to go to.

Your job is to take as an input a listing of the students' names and available
shifts, and compute an assignment of students to shifts that satisfies the
constraints.  Obviously in this problem, the number of students must be the
same as the number of shifts.

Example input:

Alice 0 1 3
Bob 1 2
Charlie 0 1 2 3
Danielle 1 2 3
"""

import collections
import sys
import copy

def ReadInputFile(filename):
  """Read a scheduling problem from a text file.

  Input format: One line per student, space-separated columns.  The first
  column is the student, the remaining columns represent the shifts that
  student is available to work.

  Example input file format:
  Alice 0 1 2 3
  Bob 1 2
  Charlie 2 3
  Danielle 3 0

  Returns:
      A map from student to a list of shifts.
  """
  with open(filename) as input_file:
    return dict((fields[0], fields[1:]) for line in input_file
        for fields in (line.split(),))

def Solve(student_availabilities):
  """Solve the constraint satisfaction problem.

  Args:
    student_availabilities: a dictionary mapping a student (a string) to a list
        of shifts in which that student can work (also strings)

  Returns:
    A dictionary mapping shifts to pairs of different students.  All times
        mentioned in the input must have entries; all students must appear
        with two different shifts, and if a shift t is mapped to student s,
        student_availabilities[s] must include t.
  """

  
  shift_available = GetShiftAvail(student_availabilities)
  shift_assigned = dict()
  for x, y in GetShiftAvail(student_availabilities).iteritems():
    print x, y

  stu_assigned = dict()
  
  stu = Search(student_availabilities)
  print "RESULT: "
  if not stu:
    print "No result."
  else:
    for x, y in GetShiftAvail(stu).iteritems():
      print x, y
  return GetShiftAvail(stu)

def Search(stu_avail):
  if stu_avail is False:

    return False
  
  if all(len(stu_avail[stu]) == 2 for stu in stu_avail.keys()):

    return stu_avail
  #chooses the student with least amount of shifts greater than 2
  n,stu = min((len(stu_avail[stu]), stu) for stu in stu_avail.keys() if len(stu_avail[stu]) > 2)

  return Some(Search(Eliminate(copy.deepcopy(stu_avail), stu, elimination))
              for elimination in stu_avail[stu])

# returns some true element of the sequence
def Some(seq):
  for e in seq:
    if e: return e
  return False

#eliminates shifts from students avaiablilities
def Eliminate(stu_avail, student, other_shift):

  if other_shift not in stu_avail[student]:
    return stu_avail
  
  stu_avail[student] = tuple(x for x in stu_avail[student] if x != other_shift)
  shift_avail = GetShiftAvail(stu_avail)

  # if a shift has less than 2 students return false
  if len(shift_avail[other_shift]) < 2:
    return False

  # if a a student has less than 2 shifts return false 
  if len(stu_avail[student]) < 2:
    return False
  
  #Constraint Propagation ***** 
  #if this student has 2 shifts and any other student in either of those shifts have only 2 shifts,
  #eliminate this shift from all other students who have it
  #if more than one student has only 2 shifts in this shift, contradiction, return false
  elif len(stu_avail[student]) == 2:

    for shift in stu_avail[student]:
      count = 0
      for stu in shift_avail[shift]:
        if not stu == student:
          if len(stu_avail[stu]) == 2:
            count = count + 1
          elif(count > 0):
            stu_avail = Eliminate(stu_avail,stu,shift)
            if not stu_avail:
              return False
          if(count > 1):
             return False
  #end added
  
  return stu_avail
  
def GetShiftAvail(student_availabilities):
  """
    Args:
      dictionary of students mapped to a list of shifts

    Returns:
      dictionary of shifts mapped to a list of students
  """
  if not student_availabilities:
    return False
  shift_availabilities = dict()

  """
  for x in range(0, len(student_availabilities)):
    shift_availabilities[str(x)] = tuple(y for y in student_availabilities.keys() if str(x) in student_availabilities[y]) 
  """
  for x,y in student_availabilities.iteritems():
    for z in y:
      if(z not in shift_availabilities):
        shift_availabilities[z] = tuple()
      a = tuple(shift_availabilities[z])
      b = x
      shift_availabilities[z] = a + (b,)
  
  return shift_availabilities


def main():
  student_availabilities = ReadInputFile(sys.argv[1])
  solution = Solve(student_availabilities)
  if solution:
    for time, (student0, student1) in solution.iteritems():
      print time, student0, student1
  else:
    print 'No satisfying assignment exists'
    
if __name__ == '__main__':
  main()
