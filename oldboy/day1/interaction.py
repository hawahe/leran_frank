
name = input("Name:")
age = int(input("Age:"))
print(type(age))
job = input("Job:")
Salary = input("Salary:")


info = '''
----------info of %s -------------
Name: %s
Age: %s
Job: %s
Salary: %s
''' %(name,name,age,job,Salary)

info2 = '''
----------info of {_name} -------------
Name: {_name}
Age: {_age}
Job: {_job}
Salary: {_Salary}
'''.format(_name=name,_age=age,_job=job,_Salary=Salary)

info3 = '''
----------info of {0} -------------
Name: {1}
Age: {2}
Job: {3}
Salary: {4}

'''.format(name,name,age,job,Salary)

print(info3)

