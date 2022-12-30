import itertools
import numpy as np

NDAYS = 5
NHOURS = 6

ALL_DAYS = range(5)
ALL_HOURS = range(6)

def NoMoreThanNClassesADay(n, classes=None):
    def verify(calendar, classes=classes):
        if not classes:
            classes = calendar.values()
        else:
            classes = [calendar[classe] for classe in classes]
        return not np.any([np.sum(classe.timetable != -1, 1) > n for classe in classes])

    return verify

def NoMoreThanNClassesADayOfSubject(n, subject, classes=None):
    def verify(calendar, classes=classes):
        if not classes:
            classes = calendar.values()
        else:
            classes = [calendar[classe] for classe in classes]
        return not np.any([np.sum(classe.timetable == subject, 1) > n for classe in classes])

    return verify



def SubjectInCertainDaysAndHours(subject, days=None, hours=None, classes=None):
    def verify(calendar, classes=classes):

        if not classes:
            classes = calendar.keys()

        all_satisfied = True

        for classe in classes:
            tt = calendar[classe].timetable
            bad_days = list(set(range(NDAYS)).difference(set(days)))
            bad_hours = list(set(range(NHOURS)).difference(set(hours)))

            if bad_days:
                satisfied_days = not np.any(tt[bad_days, :] == subject)
            else:
                satisfied_days = True

            if bad_hours:
                satisfied_hours = not np.any(tt[:, bad_hours] == subject)
            else:
                satisfied_hours = True

            if not (satisfied_days and satisfied_hours):
                all_satisfied = False

        return all_satisfied

    return verify


def NoSameTeacherForTwoClasses(first, first_subject, second, second_subject):
    def verify(calendar):
        t1 = calendar[first].timetable
        t2 = calendar[second].timetable

        return not np.any((t1 == first_subject) * (t2 == second_subject))

    return verify


# def NoSameSubject(subject, first, second):
# 	def verify(calendar):
# 		t1 = calendar[first].timetable
# 		t2 = calendar[second].timetable

# 		return not np.any((t1 == t2)[t1==subject])

# 	return verify


def NoSameSubject(subject, first, second):
    t1 = first.timetable
    t2 = second.timetable

    return not np.any((t1 == t2)[t1 == subject])


def NoSameSubjectForAnyone(subject):
    def verify(calendar):
        pairs = list(itertools.combinations(calendar.values(), 2))
        return np.all([NoSameSubject(subject, c1, c2) for c1, c2 in pairs])

    return verify


def NoSameTime(first, second):
    def verify(calendar):
        t1 = calendar[first].timetable
        t2 = calendar[second].timetable

        return not np.any(np.multiply((t1 != -1),(t2 != -1)))
    return verify


def NoSubjectOnDay(classes, subject, day):
    return not np.any([subject in c.timetable[day, :] for c in classes])


def NotBusyOnDaysAndHours(classe, days, hours):
    def verify(calendar):
        return not np.any(calendar[classe].timetable[days, hours] != -1)

    return verify


def NoMoreThanNHoursForTeacher(N, subjects, classe):
    def verify(calendar):
        t = calendar[classe].timetable
        #print(t)
        #print(t == subjects[0])
        #print(np.sum(t == subjects[0], 1))
        return not np.any(np.sum([np.sum(t == subject, 1) for subject in subjects], 0) > N)

    return verify

