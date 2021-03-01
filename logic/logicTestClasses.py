# logicTestClasses.py
# ----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import testClasses
import ast
import cnf

# Simple test case which evals an arbitrary piece of python code.
# The test is correct if the output of the code given the student's
# solution matches that of the instructor's.
class EvalTest(testClasses.TestCase):

    def __init__(self, question, testDict):
        super(EvalTest, self).__init__(question, testDict)
        self.preamble = compile(testDict.get('preamble', ""), "%s.preamble" % self.getPath(), 'exec')
        self.test = compile(testDict['test'], "%s.test" % self.getPath(), 'eval')
        self.success = testDict['success']
        self.failure = testDict['failure']

    def evalCode(self, moduleDict):
        bindings = dict(moduleDict)
        exec(self.preamble, bindings)
        return str(eval(self.test, bindings))

    def execute(self, grades, moduleDict, solutionDict):
        result = self.evalCode(moduleDict)
        if result == solutionDict['result']:
            grades.addMessage('PASS: %s' % self.path)
            grades.addMessage('\t%s' % self.success)
            return True
        else:
            grades.addMessage('FAIL: %s' % self.path)
            grades.addMessage('\t%s' % self.failure)
            grades.addMessage('\tstudent result: "%s"' % result)
            grades.addMessage('\tcorrect result: "%s"' % solutionDict['result'])

        return False

    def writeSolution(self, moduleDict, filePath):
        handle = open(filePath, 'w')
        handle.write('# This is the solution file for %s.\n' % self.path)
        handle.write('# The result of evaluating the test must equal the below when cast to a string.\n')

        handle.write('result: "%s"\n' % self.evalCode(moduleDict))
        handle.close()
        return True


class CNFTest(testClasses.TestCase):

    def __init__(self, question, test_dict):
        super(CNFTest, self).__init__(question, test_dict)
        self.preamble = compile(test_dict.get('preamble', ''), '%s.preamble' % self.getPath(), 'exec')
        self.test = compile(test_dict['test'], '%s.test' % self.getPath(), 'eval')
        self.description = test_dict['description']

        self.literals = set(ast.literal_eval(test_dict['literals'])) if 'literals' in test_dict else None
        self.clauses  = int(test_dict['clauses']) if 'clauses' in test_dict else None

        self.minsize = int(test_dict['minsize']) if 'minsize' in test_dict else None
        self.minsize_msg = test_dict['minsize_msg'] if 'minsize_msg' in test_dict else None
        self.maxsize = int(test_dict['maxsize']) if 'maxsize' in test_dict else None
        self.maxsize_msg = test_dict['maxsize_msg'] if 'maxsize_msg' in test_dict else None

        self.satisfiable = ast.literal_eval(test_dict['satisfiable']) if 'satisfiable' in test_dict else None

        self.entailment = int(test_dict['entailment']) if 'entailment' in test_dict else None
        self.entails = ast.literal_eval(test_dict['entails']) if 'entails' in test_dict else None

    def eval_code(self, module_dict):
        bindings = dict(module_dict)
        exec(self.preamble, bindings)
        return eval(self.test, bindings)

    def execute(self, grades, module_dict, solution_dict):
        grades.addMessage('TEST: %s' % self.path)
        grades.addMessage('\t%s' % self.description)
        depth = lambda L: isinstance(L, (list, tuple)) and (max(map(depth, L)) + 1 if len(L) > 0 else 0)
        value = lambda L: all(map(value, L)) if isinstance(L, (list, tuple)) else isinstance(L, int)

        result = self.eval_code(module_dict)
        if depth(result) != 2 or not value(result):
            grades.addMessage('FAIL: %s' % self.path)
            grades.addMessage('\tknowledge base is not in valid CNF form')
            return False

        if self.literals is not None:
            usage = [item for sl in result for item in sl]
            if not all([abs(x) in self.literals for x in usage]):
                grades.addMessage('FAIL: %s' % self.path)
                grades.addMessage('\tknowledge base contains literals that are unrelated')
                return False

        if self.clauses is not None:
            if len(result) != self.clauses:
                grades.addMessage('FAIL: %s' % self.path)
                grades.addMessage('\tknowledge base should contain %s clauses' % self.clauses)
                return False

        if self.minsize is not None:
            sizes = [len(x) for x in result]
            if len(sizes) == 0 or min(sizes) < int(self.minsize):
                grades.addMessage('FAIL: %s' % self.path)
                grades.addMessage('\t%s' % self.minsize_msg)
                return False

        if self.maxsize is not None:
            sizes = [len(x) for x in result]
            if len(sizes) == 0 or max(sizes) > int(self.maxsize):
                grades.addMessage('FAIL: %s' % self.path)
                grades.addMessage('\t%s' % self.maxsize_msg)
                return False

        if self.satisfiable is not None:
            sat = cnf.satisfiable(result)
            if sat != self.satisfiable:
                grades.addMessage('FAIL: %s' % self.path)
                if self.satisfiable:
                    grades.addMessage('\tknowledge base is not satisfiable (and should be)')
                else:
                    grades.addMessage('\tknowledge base is satisfiable (and should not be)')
                return False

        if self.entailment is not None:
            ent = cnf.entails(result, self.entailment)
            if ent != self.entails:
                grades.addMessage('FAIL: %s' % self.path)
                if self.entails:
                    grades.addMessage('\tknowledge base does not entail %s, but should' % self.entailment)
                else:
                    grades.addMessage('\tknowledge base entails %s, but should not' % self.entailment)
                return False


        grades.addMessage('PASS: %s' % self.path)
        return True
