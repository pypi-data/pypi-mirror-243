import ipywidgets as widgets
import random as rd
import numpy as np
import sympy
import copy
from IPython.display import Image


##########
##########
##########
#class for homework 3
##########
##########
##########

class homework_three():
#class homework_three_test():
    def __init__(self, stdID):
        # Check if Student-ID is an integer and if the function is to be run in "test-mode"
        
        #'TEst-Mode' is activated by the Std-ID input: 123456789
        # For this to be viable, 123456789 CANNEVER be a viable student-id
        if type(stdID) == int and stdID == 123456789:
            self.stdID = "testing"
        elif type(stdID) == int and stdID != 123456789:
            self.stdID = stdID
        else:
            print("Student ID required to be an integer.\nPlease try again!\n\n")
            pass
        
        # How many rngs are to be created for new/changed parameters
        self.numberofrandomnumbers = 6
        
        # Create RNs on the basis of the studentID
        self.initiate_homework()
        
        # Create variables using the generated RNs
        self.create_question_variables()
        
        # List of self.parameters:
        #self.stID
        #self.listofrndms
        
        #self.newYxs
        #self.newH
        #self.newO
        #self.newN
        
        #self.newRO2
        #self.newRCO2
        
        self.hq1tgl = 0 #help_question_1_toggle
        self.hq2tgl = 0 #help_question_2_toggle
        
        # build widgets for the questions
        self.question_one_display = self.build_question_one()
        self.question_two_display = self.build_question_two()
        
        
    def initiate_homework(self):
    # Parameters:
    # stdID is an integer used to seed the rng
        # IF stdID is given the string "test", it's supposed to return the string "test"
        # This string is then used to thest functions using standard values
    # counter is an integer used to define how many rngs are created.
        #print("Matriculation-Number accepted.\n\nGenerating random numbers..")
        #print("Matriculation-Number accepted.\n\nGenerating personalized homework parameters..")
        if self.stdID == "testing":
            print("#####\n\nTesting functionality\n\n#####")
            print("#####\n\The Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
            # NOTE: no self.listofrndms is created in test mode
        else:
        #RNG for this homework
        #IMPORTANT: rd.seed() is set GLOBALLY, as far as we observed
        #this means: the solution-codes are ALWAYS IDENTICAL FOR A UNIQUE STid
        #if rd.seed() is not refreshed after generation of listofrndms.
        #In this version, the generated solution-codes are supposed to be random, therefore. rd.seed() gets refreshed
            rd.seed(self.stdID)
            self.listofrndms = [rd.random() for i in range(self.numberofrandomnumbers)] #create new random numbers that can be used to modify parameters
            rd.seed()
        return
    
    def create_question_variables(self):
        #function returns all generated homework parameters and a boolean 
        #thats used to toggls help_question_1_toggle to  0 (helpoption was not used)
        if self.stdID != "testing":
            #print("\nGenerating personalized homework parameters...\n")
            ###PARAMATERS for QUESTION 1
            self.newYxs = 1+round(self.listofrndms[0],1) #range 1.0-2.0
            self.newH = 1.5+round((self.listofrndms[1]*0.5),1) #range 1.5-2.0
            self.newO = 0.3+round((self.listofrndms[2]*0.4),1) #range 0.3-0.7
            self.newN = 0.1+round((self.listofrndms[3]*0.2),1) #range 0.1-0.3

            ###PARAMATERS for QUESTION 2
            self.newRO2 = 3000+round((self.listofrndms[4]*500)) #range 3000-3500)
            self.newRCO2 = 8000+round((self.listofrndms[5]*500)) #range 8000-8500)
        
        elif self.stdID == "testing":
            ###PARAMATERS for QUESTION 1
            self.newYxs = 2
            self.newH = 1.8
            self.newO = 0.5
            self.newN = 0.2
            
            ###PARAMATERS for QUESTION 2
            self.newRO2 = 3300
            self.newRCO2 = 8300
        return
    
    
###############
###############
###############
    def correct_homework_three_question_one(self, RQ):
        #Parameters:
        #RQ: Student solution. Will be comparied with opimal solution and decides if task was done correctly or not
        
        #newYxs, newH, newO, newN: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq1tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? [yes] (randrange(5,9) or [no] randrange(0,4)
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) [<10] randrange(0,4)) OR [>= 10] randrange(5,9)):
        #    -> 2x randomint
        if self.stdID == "testing":
            with self.question_one_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")

                Yxc = self.newYxs - 1
                print("\nYxc:",Yxc)
                Yxn = self.newN
                Yxw = (self.newYxs*2 + Yxn*3 - self.newH)/2
                print("\nYxw:",Yxw)
                Yxo = (-self.newYxs + Yxw + 2*Yxc + self.newO)/2
                print("\nYxo:",Yxo)

                realRQ = Yxc/Yxo
                print("\nrealRQ:",realRQ)        
        
        
        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)


            #Calculation of the solution:
            with self.question_one_display.children[-1]:

                Yxc = self.newYxs - 1
                #print(Yxc)
                Yxn = self.newN
                Yxw = (self.newYxs*2 + Yxn*3 - self.newH)/2
                #print(Yxw)
                Yxo = (-self.newYxs + Yxw + 2*Yxc + self.newO)/2
                #print(Yxo)

                realRQ = Yxc/Yxo
                #print(realRQ)

                #Check if student solution is correct
                #Assumes aswer was rounded to 2 decimals
                if round(realRQ,2) == RQ:
                    self.question_one_display.children[-3].children[0].disabled = True
                    self.question_one_display.children[-3].children[1].disabled = True
                    print("Solution corect! RQ is {}".format(round(realRQ,2)))

                    solcode = ""
                     #Help-option was not used
                    if self.hq1tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq1tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 

                #If the solution was not correct, the students can try again
                else:
                    print("Solution WRONG!\nDon't give up and try again!")
                    self.question_one_display.children[-1].clear_output(wait=True)



###############
###############
###############
    def correct_homework_three_question_two(self,Yield_Ethanol, Yield_Substrate):
        #Parameters:
        #Yield_Ethanol, Yield_Substrate: Student solution. Will be comparied with opimal solution and decides if task was done correctly or not
        #ewYxs, newH, newO, newN, newRO2, newRCO2: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq2tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint

        if self.stdID == "testing":
            with self.question_two_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")


                #1. Converting biomass concentration from g/l to c-mol
                Xn = (round(46.5/(1*12+self.newH*1+self.newO*16+self.newN*14),2)*10000) 
                print("\nXn:",Xn)
                #Xn = ((50 g/L - 7 % ash)/(masses of C_1+H_newH+O_newO+N_newN) g/mol) * 10000 L = x cmol
                # 12, 1, 16, and 14 are the assumed molecular masses of the specific elements

                #2. Normalizing gas exchange rates
                rO2 = round(self.newRO2/Xn,2)
                rCO2 = round(self.newRCO2/Xn,2)
                print("\nrO2:",rO2)
                print("\nrCO2:",rCO2)

                #3. Calculating Yields, YXO, YXC
                mu = 0.35 #Growthrate = 0.35 1/h
                Yxo = round(rO2/mu,2)
                Yxc = round(rCO2/mu,2)
                Yxn = self.newN
                print("\nYxo:",Yxo)
                print("\nYxc:",Yxc)
                Ymatrixvar = np.array([[2,1],[1,-0.5]])
                Ymatrixsolvd = np.array([-1*(self.newH-2-2*Yxc-3*Yxn), -1*(self.newO+1*Yxc-1-2*Yxo)])
                Ymatrix = np.linalg.solve(Ymatrixvar,Ymatrixsolvd)
                Yxw,Yxe = Ymatrix
                Yxs = Yxe+1+Yxc
                print("\nYxe:",Yxe)
                print("\nYxs:",Yxs)

        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_two_display.children[-1]:

                #1. Converting biomass concentration from g/l to c-mol
                Xn = (round(46.5/(1*12+self.newH*1+self.newO*16+self.newN*14),2)*10000) 
                #Xn = ((50 g/L - 7 % ash)/(masses of C_1+H_newH+O_newO+N_newN) g/mol) * 10000 L = x cmol
                # 12, 1, 16, and 14 are the assumed molecular masses of the specific elements

                #2. Normalizing gas exchange rates
                rO2 = round(self.newRO2/Xn,2)
                rCO2 = round(self.newRCO2/Xn,2)

                #3. Calculating Yields, YXO, YXC
                mu = 0.35 #Growthrate = 0.35 1/h
                Yxo = round(rO2/mu,2)
                Yxc = round(rCO2/mu,2)
                Yxn = self.newN

                Ymatrixvar = np.array([[2,1],[1,-0.5]])
                Ymatrixsolvd = np.array([-1*(self.newH-2-2*Yxc-3*Yxn), -1*(self.newO+1*Yxc-1-2*Yxo)])
                Ymatrix = np.linalg.solve(Ymatrixvar,Ymatrixsolvd)
                Yxw,Yxe = Ymatrix
                Yxs = Yxe+1+Yxc

                #Check if student solution is correct
                #Assumes aswer was rounded to 2 decimals
                if round(Yxs,2) == Yield_Substrate and round(Yxe,2) == Yield_Ethanol:
                    self.question_two_display.children[-3].children[0].disabled = True
                    self.question_two_display.children[-3].children[1].disabled = True
                    print("Solution corect! Substrate yield is {}\nand Ethanol yield is {}".format(round(Yxs,2),round(Yxe,2)))

                    solcode = ""
                    #Help-option was not used
                    if self.hq2tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq2tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 

                #If the solution was not correct, the students can try again
                elif round(Yxs,2) == Yield_Substrate and round(Yxe,2) != Yield_Ethanol:
                    print("Ethanol yield WRONG!\nPlease try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)
                elif round(Yxs,2) != Yield_Substrate and round(Yxe,2) == Yield_Ethanol:
                    print("Substrate yield WRONG!\nPlease try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)
                else:
                    #print("Real Yxe={}\nStudent_Ethanol_Yield={}".format(Yxe,Yield_Ethanol))
                    #print("Real Yxs={}\nStudent_Substrate_Yield={}".format(Yxs,Yield_Substrate))
                    print("Solution WRONG!\nDon't give up and try again!")
                    self.question_two_display.children[-1].clear_output(wait=True)

    ######
    # functions that create widgets
    #
    #
    #
    ###
    
    def build_question_one(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input (top 1)
        # build 'Check Answer button' (top 2.hbox-0)
        # build 'Get help button' (top 2. hbox-1)
        # build output (for commentsof help button) (top 3)
        # build output (for answer button feedback) (top 4)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            #print("##########\n\nParameters for Question 1:\n\n"\
            #"Your glucose yield Y_(XS) is {} C-mol glucose/C-mol biomass\n\n"\
            #"Your biomass composition is CH_({})O_({})N_({})\n\n##########".format(self.newYxs,self.newH,self.newO,self.newN))
            print("")
            
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='RQ:',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))


        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check RQ',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                 
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
###############
###############
###############
    def build_question_two(self):
            listofwidgets = []

            # build question label/output (top 0)
            # build answer input for Ethanol Yield (top 1)
            # build answer input for Substrate Yield (top 2)
            # build 'Check Answer button' (top 3.hbox-0)
            # build 'Get help button' (top 3. hbox-1)
            # build output (for commentsof help button) (top 4)
            # build output (for answer button feedback) (top 5)

            listofwidgets.append(widgets.Output(
            ))
            with listofwidgets[0]:
                #print("##########\n\nParameters for Question 2:\n\n"\
                #"Your O_2 Exchange-Rate is {} mol/h\n\n"\
                #"Your CO_2 Exchange-Rate is {} mol/h\n\n##########".format(self.newRO2,self.newRCO2))
                print("")
                
            listofwidgets.append(widgets.FloatText(
                value=0.00,
                description='Ethanol Yield:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='200px', height='40px')
            ))
            
            listofwidgets.append(widgets.FloatText(
                value=0.00,
                description='Substrate Yield:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='200px', height='40px')
            ))


            i = []
            i.append(widgets.Button(
                value=False,
                description='Check Yields',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to check solution',
                #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            i.append(widgets.Button(
                value=False,
                description='Calculation Help',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to get a tipp',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            listofwidgets.append(widgets.HBox(i))

            listofwidgets.append(widgets.Output())
            listofwidgets.append(widgets.Output())

            disp = widgets.VBox(listofwidgets)
            return disp
    
    ######
    # ON-CLICK functions
    # 2 per question
    #
    #
    ###
    def on_question_one_help_button_clicked(self, click):
        self.hq1tgl = 1
        self.question_one_display.children[-3].children[1].disabled = True
        with self.question_one_display.children[-2]:
            txt = "##########\n" \
            "* The RQ is rate of CO_2 production divivided by the rate of O_2 production\n" \
            "  RQ = r(CO_2)/r(O_2)\n\n" \
            "* Yields correlate directly to rates\n" \
            "  RQ = r(CO_2)/r(O_2) = Y(CO_2)/Y(O_2)\n\n" \
            "* By calculating all yields for the known reaction, you will be able to identify the required yields\n" \
            "##########"
            print(txt)
    def on_question_one_answer_button_clicked(self, click):
        student_answer = self.question_one_display.children[1].value
        self.correct_homework_three_question_one(student_answer)
        
    def on_question_two_help_button_clicked(self, click):
        self.hq2tgl = 1
        self.question_two_display.children[-3].children[1].disabled = True
        with self.question_two_display.children[-2]:
            txt = "##########\n" \
            "Don't forget, that for Question 2, Ethanol is an additional product!\nYou also need to subtract the ash from the assumed Biomass.\n\n"\
            "* First, convert the biomass concentration from g/L to c-mol\n" \
            "  and normalize the gas exchange rates\n\n" \
            "* You can use the growth rates and exchange rates to determine\n the yields of O_2 and CO_2\n\n" \
            "* How to solve the matrix can be seen in 'Example 1' (p. 19/20 of Lecture QM3 ‘Quantitative Microbiologie week 4 – Folien’)\n"
            "##########\n"
            print(txt)
    def on_question_two_answer_button_clicked(self, click):
        student_answer_ethanol_yield = self.question_two_display.children[1].value
        student_answer_substrate_yield = self.question_two_display.children[2].value
        self.correct_homework_three_question_two(student_answer_ethanol_yield, student_answer_substrate_yield)

##########
##########
##########
#class for homework 4
##########
##########
##########

class homework_four():
#class homework_four_test():
    def __init__(self, stdID):
        # Check if Student-ID is an integer and if the function is to be run in "test-mode"
        
        #'TEst-Mode' is activated by the Std-ID input: 123456789
        # For this to be viable, 123456789 CAN NEVER be a viable student-id
        if type(stdID) == int and stdID == 123456789:
            self.stdID = "testing"
        elif type(stdID) == int and stdID != 123456789:
            self.stdID = stdID
        else:
            print("Student ID required to be an integer.\nPlease try again!\n\n")
            pass
        
        # How many rngs are to be created for new/changed parameters
        self.numberofrandomnumbers = 8
        
        # Create RNs on the basis of the studentID
        self.initiate_homework()
        
        # Create variables using the generated RNs
        self.create_question_variables()
        
        # List of self.parameters:
        #self.stID
        #self.listofrndms
        
        #self.newCoP (CombustionofProtein)
        #self.newCoC (CombustionofCarbohydrates)
        #self.newCoF (CombustionofFat)
        
        #self.newOCR (OxygenConsumptionrate)
        #self.newCPR (Carbon dioxide production rate)
        #self.newNSR (Nitrogen secretion rate)
        
        self.hq1tgl = 0 #help_question_1_toggle
        self.hq2tgl = 0 #help_question_2_toggle
        self.hq3tgl = 0 #help_question_2_toggle
        
        # build widgets for the questions
        self.question_one_display = self.build_question_one()
        self.question_two_display = self.build_question_two()
        self.question_three_display = self.build_question_three()
        
        
    def initiate_homework(self):
    # Parameters:
    # stdID is an integer used to seed the rng
        # IF stdID is given the string "test", it's supposed to return the string "test"
        # This string is then used to thest functions using standard values
    # counter is an integer used to define how many rngs are created.
        #print("Matriculation-Number accepted.\n\nGenerating random numbers..")
        #print("Matriculation-Number accepted.\n\nGenerating personalized homework parameters..")
        if self.stdID == "testing":
            print("#####\n\nTesting functionality\n\n#####")
            print("#####\n\The Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
            # NOTE: no self.listofrndms is created in test mode
        else:
        #RNG for this homework
        #IMPORTANT: rd.seed() is set GLOBALLY, as far as we observed
        #this means: the solution-codes are ALWAYS IDENTICAL FOR A UNIQUE STid
        #if rd.seed() is not refreshed after generation of listofrndms.
        #In this version, the generated solution-codes are supposed to be random, therefore. rd.seed() gets refreshed
            rd.seed(self.stdID)
            self.listofrndms = [rd.random() for i in range(self.numberofrandomnumbers)] #create new random numbers that can be used to modify parameters
            rd.seed()
        return
    
    def create_question_variables(self):
        #function returns all generated homework parameters and a boolean 
        #thats used to toggls help_question_1_toggle to  0 (helpoption was not used)
        if self.stdID != "testing":
            #print("\nGenerating personalized homework parameters...\n")
            ###PARAMATERS for QUESTION 1
            self.newCoP = 4.0+round((self.listofrndms[0]*0.2),1) #range 4.0-4.2
            self.newCoC = 4.0+round((self.listofrndms[1]*0.3),1) #range 4.0-4.3
            self.newCoF = 9.0+round((self.listofrndms[2]*0.6),1) #range 9.0-9.6

            ###PARAMATERS for QUESTION 3
            self.newOCR = 0.5+round((self.listofrndms[4]*0.2)) #range 0.5-0.7)
            self.newCPR = 0.4+round((self.listofrndms[5]*0.2)) #range 0.4-0.6)
            self.newNSR = 0.05+round((self.listofrndms[6]*0.2)) #range 0.05-0.25)
            
        elif self.stdID == "testing":
            ###PARAMATERS for QUESTION 1
            self.newCoP = 4.1 #(CombustionofProtein [kcal/g])
            self.newCoC = 4.2 #(CombustionofCarbohydrates [kcal/g])
            self.newCoF = 9.3 #(CombustionofFat [kcal/g])
            
           ###PARAMATERS for QUESTION 3
            self.newOCR = 0.6 #(OxygenConsumptionrate [mol/h])
            self.newCPR = 0.52 #(Carbon dioxide production rate [mol/h])
            self.newNSR = 0.1 #(Nitrogen secretion rate [N/h])

        return
    
    
###############
###############
###############
    def correct_homework_four_question_one(self, YxqP, YxqC, YxqF):
        #Parameters:
        #YxqP, YxqC, YxqF: Student solutions. Will be comparied with opimal solution and decides if task was done correctly or not
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq1tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        if self.stdID == "testing":
            with self.question_one_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")

                mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
                mc = 12+2+16 #CH_2O
                mf = 12+1.92+16*0.12 #CH_1.92O_0.12
                
                print(self.newCoP * mp)
                print(self.newCoC * mc)
                print(self.newCoF * mf)
        
        
        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)


            #Calculation of the solution:
            with self.question_one_display.children[-1]:

                mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
                mc = 12+2+16 #CH_2O
                mf = 12+1.92+16*0.12 #CH_1.92O_0.12
            
                #Check if student solutions are correct
                counter = 0
                #Assumes aswer was rounded to 2 decimals
                if round(mp*self.newCoP,2) != YxqP:
                    counter += 1
                    print("Wrong Combustion of Protein\n")
                if round(mc*self.newCoC,2) != YxqC:
                    counter += 1
                    print("Wrong Combustion of Carbohydrates\n")
                if round(mf*self.newCoF,2) != YxqF:
                    counter += 1
                    print("Wrong Combustion of Fat\n")
                if round(mp*self.newCoP,2) == YxqP and round(mc*self.newCoC,2) == YxqC and round(mf*self.newCoF,2) == YxqF:
                    self.question_one_display.children[-3].children[0].disabled = True
                    self.question_one_display.children[-3].children[1].disabled = True
                    print("Solution corect!")

                    solcode = ""
                    #Help-option was not used
                    if self.hq1tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq1tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.") 

                if counter != 0:
                    print("\n##########\n Don't give up and try again!\n\n")
                    self.question_one_display.children[-1].clear_output(wait=True)


###############
###############
###############
    def correct_homework_four_question_two(self,student_answer_Ycs, student_answer_Ycf, student_answer_Ycp):
        #Parameters:
        #Yield_sugar (student_answer_Ycs), Yield_fat: student_answer_Ycf, Yield_protein student_answer_Ycp
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
        #newOCR, newCPR, newNSR: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq2tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        
        
        # Hopefully temporary: list of solutions for all three Yields
        # In this HW_4 section, no parameters were changed yet.
        # Thus, the literature solutions arethe correct solutions
        #format: 
        #Y_cs = {A} + {B}*Y_co + {C}*Y_cn"
        #sol_Ycs= [A, B, C]
        sol_Ycs = [-2.38,3.38,-3.58]
        sol_Ycf = [2.38,-2.38,-0.27]
        sol_Ycp = [0.0,0.0,3.85]
        
        
        if self.stdID == "testing":
            with self.question_two_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
                
                print("Yield sugar/carbohydrates: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycs[0],sol_Ycs[1],sol_Ycs[2]))
                print("Yield fat: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycf[0],sol_Ycf[1],sol_Ycf[2]))
                print("Yield protein: {} + {}*Y_co + {}*Y_c\n\n".format(sol_Ycp[0],sol_Ycp[1],sol_Ycp[2]))

        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_two_display.children[-1]:
                counter = 0
                
                print("Y_cs: {1} + {2} * Y_co + {3} * Y_cn\n-----------------------------\n")
                for i in range(len(student_answer_Ycs)):
                    if round(student_answer_Ycs[i],1) != round(sol_Ycs[i],1):
                        counter += 1
                        print('Variable {} is WRONG\n'.format(i+1))
                print("Y_cf: {1} + {2} * Y_co + {3} * Y_cn\n-----------------------------\n")
                for i in range(len(student_answer_Ycf)):
                    if round(student_answer_Ycf[i],1) != round(sol_Ycf[i],1):
                        counter += 1
                        print('Variable {} is WRONG\n'.format(i+1))
                print("Y_cp: {1} + {2} * Y_co + {3} * Y_cn\n-----------------------------\n")
                for i in range(len(student_answer_Ycp)):
                    if round(student_answer_Ycp[i],1) != round(sol_Ycp[i],1):
                        counter += 1
                        print('Variable {} is WRONG\n'.format(i+1))
                if counter != 0:
                    print("\n##########\n Don't give up and try again!\n\n")
                    self.question_two_display.children[-1].clear_output(wait=True)
                elif counter == 0:
                    self.question_two_display.children[-3].children[0].disabled = True
                    self.question_two_display.children[-3].children[1].disabled = True
                    print("Solution correct!")

                    solcode = ""
                    #Help-option was not used
                    if self.hq2tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq2tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.")

###############
###############
###############
    def correct_homework_four_question_three(self,student_answer_Yco, student_answer_Ycn, student_answer_Rxq):
        #Parameters:
        #Yield_co (student_answer_Yco) normalized to CO2, Yield_cn: student_answer_Ycn normalized to CO2, metablic rate student_answer_Rxq (kcal/h)
        
        #newCoP, newCoC, newCoF: changed parameters based on the seed.
        #newOCR, newCPR, newNSR: changed parameters based on the seed.
            #are needed to calculate the opimal solution
        #hq3tgl: boolean. Decides if the student used the help-option or not
        
        #ALSO:
        # Instead of a literature solution matrix, the student solution of Question 2 is to be used as a basis
        # So that they can get points for Question 3, even if they got Question 2 wrong

        #output formula:
        # X-YZ
        # X: was the help used? yes or no
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) <10 OR >= 10:
        #    -> 2x randomint
        
        
        # Hopefully temporary: list of solutions for all three Yields
        # In this HW_4 section, te parameters of the chemical composition parameters were not changed yet.
        # Thus, the literature solutions are the correct solutions of Homework_4_2:
        #format: 
        #Y_cs = {A} + {B}*Y_co + {C}*Y_cn"
        #sol_Ycs= [A, B, C]
        #sol_Ycs = [-2.38,3.38,-3.58]
        #sol_Ycf = [2.38,-2.38,-0.27]
        #sol_Ycp = [0.0,0.0,3.85]     
        
        mp = 12+1.57+16*0.32+14*0.26 #CH_1.57O_0.32N_0.26
        mc = 12+2+16 #CH_2O
        mf = 12+1.92+16*0.12 #CH_1.92O_0.12
        
        if self.stdID == "testing":
            with self.question_three_display.children[0]:
                print('\nTesting solution calculation...\n')
                print("#####\n\nThe Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
                
                Ycc = round(self.newCPR/self.newCPR,2) #(mol/h / mol/h)
                Yco = round(self.newOCR/self.newCPR,2) #(mol/h / mol/h)
                rn = self.newNSR/14 #(Secretion rate NH3 in gN/h / 14 g/mol)
                Ycn = round(rn/self.newCPR,2) #(mol/h / mol/h)
                
                print('Yco: \n',Yco)
                print('Ycn: \n',Ycn)
                
                Ycs = round(sol_Ycs[0]*Ycc+sol_Ycs[1]*Yco+sol_Ycs[2]*Ycn,2) #(mol/cmol)
                Ycf = round(sol_Ycf[0]*Ycc+sol_Ycf[1]*Yco+sol_Ycf[2]*Ycn,2) #(mol/cmol)
                Ycp = round(sol_Ycp[0]*Ycc+sol_Ycp[1]*Yco+sol_Ycp[2]*Ycn,2) #(mol/cmol)
                
                print('Ycs: \n',Ycs)
                print('Ycf: \n',Ycf)
                print('Ycp: \n',Ycp)
                print('mc: \n', mc)
                print('mf: \n', mf)
                print('mp: \n', mp)
                
                Yxq = Ycs*round(mc*self.newCoC,2)+Ycf*round(mf*self.newCoF,2)+Ycp*round(mp*self.newCoP,2) #(mol/cmol * kcal/cmol) = (kcal/cmol) || units not clear, might need second look
                Rxq = round(Yxq * self.newCPR,2) # kcal/cmol * mol/h = kcal/h || units not clear, might need second look
                
                print('Yxq: \n',Yxq)
                print('Rxq: \n',Rxq)


        if type(self.stdID) == int:
            stdIDstr = str(self.stdID)
            
            #Calculation of the solution:
            with self.question_three_display.children[-1]:
                
                # Instead of a literature solution, the student solution is to be used as a basis
                # So that they can get points for Question 3, even if they got Question 2 wrong
                sol_Ycs = []
                sol_Ycf = []
                sol_Ycp = []
                for i in self.question_two_display.children[2].children:
                    sol_Ycs.append(i.value)
                for i in self.question_two_display.children[4].children:
                    sol_Ycf.append(i.value)
                for i in self.question_two_display.children[6].children:
                    sol_Ycp.append(i.value)
                #RUDIMENTARY check if there are problems with the student solution of Question 2
                checkcounter = 0
                if sum(sol_Ycs) == 0:
                    checkcounter += 1
                if sum(sol_Ycf) == 0:
                    checkcounter += 1
                if sum(sol_Ycp) == 0:
                    checkcounter += 1
                    
                if checkcounter > 0:
                    print("\n##########\nNo Solution of Question 2 detected!\nPlease try to solve Question 2 before answering Question 3!\n\n")
                    self.question_three_display.children[-1].clear_output(wait=True)
                    return
                    
                #if Question 2 answers are accepted, continue here    
                Ycc = round(self.newCPR/self.newCPR,2) #(mol/h / mol/h)
                Yco = round(self.newOCR/self.newCPR,2) #(mol/h / mol/h)
                rn = self.newNSR/14 #(Secretion rate NH3 in gN/h / 14 g/mol)
                Ycn = round(rn/self.newCPR,2) #(mol/h / mol/h)
                
                #Check first Checkpoint
                counter = 0
                if Yco != student_answer_Yco:
                    counter += 1
                    print("Normalized Yield_co WRONG!\n")
                if Ycn != student_answer_Ycn:
                    counter += 1
                    print("Normalized Yield_cn WRONG!\n")

                       
                Ycs = round(sol_Ycs[0]*Ycc+sol_Ycs[1]*Yco+sol_Ycs[2]*Ycn,2) #(mol/cmol)
                Ycf = round(sol_Ycf[0]*Ycc+sol_Ycf[1]*Yco+sol_Ycf[2]*Ycn,2) #(mol/cmol)
                Ycp = round(sol_Ycp[0]*Ycc+sol_Ycp[1]*Yco+sol_Ycp[2]*Ycn,2) #(mol/cmol)
                

                Yxq = Ycs*round(mc*self.newCoC,2)+Ycf*round(mf*self.newCoF,2)+Ycp*round(mp*self.newCoP,2) #(mol/cmol * kcal/cmol) = (kcal/cmol) || units not clear, might need second look
                Rxq = round(Yxq * self.newCPR,2) # kcal/cmol * mol/h = kcal/h || units not clear, might need second look
                
                #Check second Checkpoint
                if Rxq != student_answer_Rxq:
                    counter += 1
                    print("Metabolic rate WRONG!\n")
                
                
                if counter != 0:
                    print("\n##########\n Don't give up and try again!\n\n")
                    self.question_three_display.children[-1].clear_output(wait=True)
                elif counter == 0:
                    self.question_three_display.children[-3].children[0].disabled = True
                    self.question_three_display.children[-3].children[1].disabled = True
                    print("Solution corect!")
                    solcode = ""
                    #Help-option was not used
                    if self.hq3tgl == 0:
                        solcode+=(str(rd.randrange(0,4)))
                    #Help-option was used
                    elif self.hq3tgl == 1:
                        solcode+=(str(rd.randrange(5,9)))

                    if int(stdIDstr[-1])+int(stdIDstr[-2]) < 10:
                        solcode+=(str(rd.randrange(0,4)))
                        solcode+=(str(rd.randrange(0,4)))
                    elif int(stdIDstr[-1])+int(stdIDstr[-2]) >= 10:
                        solcode+=(str(rd.randrange(5,9)))
                        solcode+=(str(rd.randrange(5,9)))    
                    # PRINT THE CODE
                    print("Here's your code!\n\n"+solcode+"\n\nPlease upload it in the designated Moodle-Task.")
                

    ######
    # functions that create widgets
    #
    #
    #
    ###
    
    def build_question_one(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input YxqP(top 1)
        # build answer input YxqC(top 2)
        # build answer input YxqF(top 3)
        # build 'Check Answer button' (top 4.hbox-0)
        # build 'Get help button' (top 4. hbox-1)
        # build output (for commentsof help button) (top 5)
        # build output (for answer button feedback) (top 6)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            #print("##########\n\nParameters for Question 1:\n\n"\
            #"Your glucose yield Y_(XS) is {} C-mol glucose/C-mol biomass\n\n"\
            #"Your biomass composition is CH_({})O_({})N_({})\n\n##########".format(self.newYxs,self.newH,self.newO,self.newN))
            print("")
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqP [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))

        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqC [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='YxqF [kcal/mol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check Solution',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
        
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
###############
###############
###############
    def build_question_two(self):
            listofwidgets = []

            # build question label/output (top 0)
            # build answer format label for Ycs (top 1)
                #build answer input for Ycs answer {A} (top 2.hbox-0)
                #build answer input for Ycs answer {B} (top 2.hbox-1)
                #build answer input for Ycs answer {C} (top 2.hbox-2)
            # build answer input for Ycf (top 3)
                #build answer input for Ycf answer {A} (top 4.hbox-0)
                #build answer input for Ycf answer {B} (top 4.hbox-1)
                #build answer input for Ycf answer {C} (top 4.hbox-2)
            # build answer input for Ycn (top 5)
                #build answer input for Ycn answer {A} (top 6.hbox-0)
                #build answer input for Ycn answer {B} (top 6.hbox-1)
                #build answer input for Ycn answer {C} (top 6.hbox-2)
            # build 'Check Answer button' (top 7.hbox-0)
            # build 'Get help button' (top 7. hbox-1)
            # build output (for commentsof help button) (top 8)
            # build output (for answer button feedback) (top 9)

            listofwidgets.append(widgets.Output(
            ))
            with listofwidgets[0]:
                #print("##########\n\nParameters for Question 2:\n\n"\
                #"Your O_2 Exchange-Rate is {} mol/h\n\n"\
                #"Your CO_2 Exchange-Rate is {} mol/h\n\n##########".format(self.newRO2,self.newRCO2))
                print("")
            ###
            # Widgtes responsible for student input of Y_cs
            ###
            listofwidgets.append(widgets.Label(
                value="Yield: Y_cs [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstOne = []
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstOne.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstOne))

            ###
            # Widgtes responsible for student input of Y_cf
            ###
            listofwidgets.append(widgets.Label(
                value="Yield: Y_cf [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstTwo = []
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstTwo.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstTwo))
            
            ###
            # Widgtes responsible for student input of Y_cp
            ###
            listofwidgets.append(widgets.Label(
                value="Yield: Y_cp [mol/cmol]= {A} + {B}*Y_co + {C}*Y_cn",
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='500px', height='40px')
            ))
            lstThree = []
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='A:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='B:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            lstThree.append(widgets.FloatText(
                value=0.0,
                description='C:',
                disabled=False,
                display='flex',
                flex_flow='column',
                align_items='stretch',
                style= {'description_width': 'initial'},
                layout = widgets.Layout(width='100px', height='40px')
            ))
            listofwidgets.append(widgets.HBox(lstThree))
            
            
            ###
            # Wisgets resonsible for Solution check and help button
            #
            i = []
            i.append(widgets.Button(
                value=False,
                description='Check Yields',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to check solution',
                #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            i.append(widgets.Button(
                value=False,
                description='Calculation Help',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to get a tipp',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            listofwidgets.append(widgets.HBox(i))

            listofwidgets.append(widgets.Output())
            listofwidgets.append(widgets.Output())

            disp = widgets.VBox(listofwidgets)
            return disp
        
###############
###############
###############        
    def build_question_three(self):
        listofwidgets = []
        
        # build question label/output (top 0)
        # build answer input Yco(top 1)
        # build answer input Ycn(top 2)
        # build answer input Rxq(top 3)
        # build 'Check Answer button' (top 4.hbox-0)
        # build 'Get help button' (top 4. hbox-1)
        # build output (for commentsof help button) (top 5)
        # build output (for answer button feedback) (top 6)
        
        listofwidgets.append(widgets.Output(
        ))
        with listofwidgets[0]:
            print("")
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Yco [mol/cmol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))

        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Ycn [mol/cmol]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        listofwidgets.append(widgets.FloatText(
            value=0.00,
            description='Rxq [kcal/h]',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='200px', height='40px')
        ))
        
        i = []
        i.append(widgets.Button(
            value=False,
            description='Check Solution',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to check solution',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
                             
        i.append(widgets.Button(
            value=False,
            description='Calculation Help',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to get a tipp',
        #     icon='check' # (FontAwesome names without the `fa-` prefix)
        ))
        
        listofwidgets.append(widgets.HBox(i))
        
        listofwidgets.append(widgets.Output())
        listofwidgets.append(widgets.Output())
        
        disp = widgets.VBox(listofwidgets)
        return disp
    
    ######
    # ON-CLICK functions
    # 2 per question
    #
    #
    ###
    def on_question_one_help_button_clicked(self, click):
        self.hq1tgl = 1
        self.question_one_display.children[-3].children[1].disabled = True
        with self.question_one_display.children[-2]:
            txt = "##########\n" \
            "Given are the estimated heat of combustions in (kcal/g) and\nthe chemical composition.\n\n" \
            "* Sum up the approximate weight of each subgroup in g/cmol\n\n" \
            "* Multiply the 'heat of combustion' (kcal/g) with the 'molecular weight' (g/mol)\n" \
            "##########"
            print(txt)
    def on_question_one_answer_button_clicked(self, click):
        student_YxqP = self.question_one_display.children[1].value
        student_YxqC = self.question_one_display.children[2].value
        student_YxqF = self.question_one_display.children[3].value
        self.correct_homework_four_question_one(student_YxqP, student_YxqC, student_YxqF)
        
    def on_question_two_help_button_clicked(self, click):
        self.hq2tgl = 1
        self.question_two_display.children[-3].children[1].disabled = True
        with self.question_two_display.children[-2]:
            txt ="""
##########\n
Given is the stoichiometry of the combustion of Carbohydrates (Ycs), Fats (Ycf), and Protein (Ycp)\ntogether with Oxygen (Yco) to form CO_2 (Ycc), ammonia (Ycn) and water (Ycw).\n
The equation is normalized on CO_2, so the yield of CO_2 (Ycc) = 1.\n
The task is to solve Ycs, Ycf and Ycp as functions of Yco and Ycn.\n
One way to do this, is to calculate the degree of reduction (DoR) as can be seen on p. 23-25 in the\nQM3-script ‘Quantitative Microbiologie week 4 – Folien’.\n
Setting up a stoichiometric matrix should look like this:\n\n
\t\t\t\t\t\t\t\tYcs\n
\t\t\t\t\t\t\t\tYcf\n
C  :\t1\t1\t1\t0\t0\t1\t\tYcp\n
N  :\t0\t0\tx\t0\t1\t0\t*\tYco\t=\t0\n
DoR:\tx\tx\tx\t4\t0\t0\t\tYcn\n
\t\t\t\t\t\t\t\tYcc\n\n

And rearranging the matrix using Gaussian elimination to get functions of Yco and Ycn should end up looking like this:\n\n
\t\t\t\t\t\t\t\tYcs\n
\t\t\t\t\t\t\t\tYcf\n
C  :\t1\t0\t0 \tB_cs\tC_cs\tA_cs\t\tYcp\n
N  :\t0\t1\t0\tB_cf\tC_cf\tA_cf\t*\tYco\t=\t0\n
DoR:\t0\t0\t1\tB_cp\tC_cp\tA_cp\t\tYcn\n
\t\t\t\t\t\t\t\tYcc\n\n
Meaning that the example-equation of Ycs looks like this: \n
Ycs + B_cs*Yco + C_cs*Ycn + A_cs*Ycc(with Ycc=1) = 0\n
Rearrange it for Ycs and repeat the procedure for Ycf and Ycn.\n
##########\n
            """

            print(txt)
            
    def on_question_two_answer_button_clicked(self, click):
        student_answer_Ycs = []
        student_answer_Ycf = []
        student_answer_Ycp = []
        for i in self.question_two_display.children[2].children:
            student_answer_Ycs.append(i.value)
        for i in self.question_two_display.children[4].children:
            student_answer_Ycf.append(i.value)
        for i in self.question_two_display.children[6].children:
            student_answer_Ycp.append(i.value)
        self.correct_homework_four_question_two(student_answer_Ycs, student_answer_Ycf, student_answer_Ycp)
        
    #def on_question_two_reset_button_clicked(self, click):
    #    #A button that, when clicked resets the value fo the input frlds to the original format, thus showing how the input has to look like
    #    self.question_two_display.children[1].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycs (top 1)
    #    self.question_two_display.children[2].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycf (top 1)
    #    self.question_two_display.children[3].value = "{A} + {B}*Y_co + {C}*Y_cn" #input for Ycn (top 1)
    #    with self.question_two_display.children[-1]:
    #        print("#####\nInput-Fields RESET\n#####")
    #        self.question_two_display.children[-1].clear_output(wait=True)
    
    def on_question_three_answer_button_clicked(self, click):
        student_Yco = self.question_three_display.children[1].value
        student_Ycn = self.question_three_display.children[2].value
        student_Rxq = self.question_three_display.children[3].value
        self.correct_homework_four_question_three(student_Yco, student_Ycn, student_Rxq)
    
    def on_question_three_help_button_clicked(self, click):
        self.hq3tgl = 1
        self.question_three_display.children[-3].children[1].disabled = True
        with self.question_three_display.children[-2]:
            txt ="""
##########\n
Task is determine the metabolic rate Rxq [kcal/h]\n
 * First step is to calculate the Yields of O_2 (Yco) and NH_4 (Ycn)relative to CO_2\n
(* The Yied of CO_2 (Y_cc) = 1 [mol/cmol])\n
(* Don’t forget to calculate Ycn out of the nitrogen secretion rate!)\n
 * Next, enter the yields into the three equations from [Question 2].\n
 * Calculate Yxq [kcal/cmol] (p. 36-38  in the QM3-script ‘Quantitative Microbiologie week 4 – Folien’\n
 * The formula for Rxq is Yxq [kcal/cmol] * r_co2 [cmol/h]\n
##########\n
            """

            print(txt)

##########
##########
##########
#class for homework 5
##########
##########
##########

class homework_five():
#class homework_five_test():
    def __init__(self):
        self.init_display = self.build_init_display()
        
        
        
    def start_homework(self, stdID):
        # Check if Student-ID is an integer and if the function is to be run in "test-mode"
        
        #'TEst-Mode' is activated by the Std-ID input: 123456789
        # For this to be viable, 123456789 CANNEVER be a viable student-id
        if type(stdID) == int and stdID == 123456789:
            self.stdID = "testing"
        elif type(stdID) == int and stdID != 123456789:
            self.stdID = stdID
        else:
            print("Student ID required to be an integer.\nPlease try again!\n\n")
            pass
        
        # How many rngs are to be created for new/changed parameters
        self.numberofrandomnumbers = 10
        
        # Create RNs on the basis of the studentID
        self.initiate_homework()
        
        # Create variables using the generated RNs
        self.create_question_variables()
        
        # List of self.parameters:
        #self.stID
        #self.listofrndms
        
        #self.v1
        #self.v4
        #self.v5
        #self.v6
        #self.v7
        
        self.hq1tgl = 0 #help_question_1_toggle
        self.hq2tgl = 0 #help_question_2_toggle
        
        # build widgets for the questions
        self.question_one_display = self.build_question_display()
        self.question_two_display = self.build_question_display()
        
        with self.init_display.children[2]:
            txt= """
##########\n\nParameters for Question 2:\n\n
Flux v1 = {}\n
Flux v4 = {}\n
Flux v5 = {}\n
Flux v6 = {}\n
Flux v7 = {}\n\n
##########
            """.format(self.v1,self.v4,self.v5,self.v6,self.v7)
            print(txt)
        
        
    def initiate_homework(self):
    # Parameters:
    # stdID is an integer used to seed the rng
        # IF stdID is given the string "test", it's supposed to return the string "test"
        # This string is then used to thest functions using standard values
    # counter is an integer used to define how many rngs are created.
        #print("Matriculation-Number accepted.\n\nGenerating random numbers..")
        #print("Matriculation-Number accepted.\n\nGenerating personalized homework parameters..")
        if self.stdID == "testing":
            print("#####\n\nTesting functionality\n\n#####")
            print("#####\n\The Std-ID is not a valid Student-ID\n and CAN'T generate a valid code!\n\n#####")
            # NOTE: no self.listofrndms is created in test mode
        else:
        #RNG for this homework
        #IMPORTANT: rd.seed() is set GLOBALLY, as far as we observed
        #this means: the solution-codes are ALWAYS IDENTICAL FOR A UNIQUE STid
        #if rd.seed() is not refreshed after generation of listofrndms.
        #In this version, the generated solution-codes are supposed to be random, therefore. rd.seed() gets refreshed
            rd.seed(self.stdID)
            self.listofrndms = [rd.random() for i in range(self.numberofrandomnumbers)] #create new random numbers that can be used to modify parameters
            rd.seed()
        return
    
    def create_question_variables(self):
        #function returns all generated homework parameters and a boolean 
        #thats used to toggls help_question_1_toggle to  0 (helpoption was not used)
        if self.stdID != "testing":
            #print("\nGenerating personalized homework parameters...\n")
            
            ###PARAMATERS for QUESTION 2           
            ### STEP 1: Create modified parameters
            self.v1 = 19+round(self.listofrndms[0]*2,1) #range 19.0-21.0
            self.v4 = 30+round(self.listofrndms[1]*2,1) #range 30.0-32.0
            self.v5 = 9+round(self.listofrndms[2]*1,1) #range 9.0-10.0
            self.v6 = 4.5+round(self.listofrndms[3]*1,1) #range 4.5.0-5.5
            self.v7 = 4.5+round(self.listofrndms[4]*1,1) #range 4.5.0-5.5 
            
            ### STEP 2: Determine if the Equations are consistent or not:
            ### MOVED TO QUESTION-2-SOLVER
                
        
        elif self.stdID == "testing":
            ###PARAMATERS for QUESTION 2
            self.v1 = 19.3
            self.v4 = 31.1
            self.v5 = 9.5
            self.v6 = 5.5
            self.v7 = 5.0
            
        return
            
###############
###############
###############
    def test_homework_five(self, litmatr, test):
        testnumber = "123456789"
        #Parameters:
        #listofbalances: Student solutions. Will be comparied with opimal solution and decides if task was done correctly or not
        #studentindep = Student solution part 2
        
        #NO parameters were changed for this question
        #hq1tgl: boolean. Decides if the student used the help-option or not

        #output formula:
        # X-YZ
        # X: was the help used? [yes] (randrange(5,9) or [no] randrange(0,4)
        #    -> randomint
        # YZ: Summ(studentID[0]+studentID[1]) [<10] randrange(0,4)) OR [>= 10] randrange(5,9)):
        #    -> 2x randomint
        if test != testnumber:
            return
        
        print("\n####\nQuestion 1\n#####\n")
        
        if litmatr == None:
        
            litmatr = [[1,-1,0,0,0,0,0,0],
            [-1,2,-1,0,0,0,0,0],
            [1,0,1,-1,-1,0,0,0],
            [0,0,0,0,1,-1,-1,0],
            [0,1,1,0,0,1,0,-1],
            [0,2,0,-1,0,0,-2,0]]
        
        #Calculate the independents of litmatr
        _, litinds = sympy.Matrix(litmatr).T.rref()
        print("Number of independent reactions in matrix:",len(litinds))
        print("Position of independent reactions in matrix:",litinds)
        
        print("\n####\nQuestion 2\n#####\n")
        

        concounter = 0
        noncon = []

        # background check relations:
        # v1 = v2 = v3 = (0.5v7 + 0.5v8)
        # 0.5v5 = v6 = v7

        # v5 - v6 - v7 = 0 --> 2v6 - v6 - v7 = 0 --> v6 - v7 = 0
        # v5 - v6 - v7 = 0 --> v5 - 2v6/2v7 = 0
        # 2v2 - v4 - 2v6 --> 2v1 - v4 -2v6/2v7 = 0

        # => 2v1 - v4 = 2v6/2v7 = v5 with v6 - v7 = 0
        p1 = [2*self.v1 - self.v4, 2*round(self.v1*0.05,2) + round(self.v4*0.05,2),"v1, v4"]
        p2 = [self.v5, round(self.v5*0.05,2),"v5"]
        p3 = [2*self.v6, round(2*self.v6*0.05,2),"v6"]
        p4 = [2*self.v7, 2*round(self.v7*0.05,2),"v7"]

        # Check 1
        if (self.v6 - self.v7) + (self.v6*0.05 + self.v7*0.05) >= 0 > (self.v6 - self.v7) - (self.v6*0.05 + self.v7*0.05) or (self.v7 - self.v6) + (self.v6*0.05 + self.v7*0.05) >= 0 > (self.v7 - self.v6) - (self.v6*0.05 + self.v7*0.05):
            concounter += 0            
        else:
            concounter += 1
            noncon.append([p3,p4])

        #Check 2 - 4
        if (p1[0]-p2[0])+(p1[1]+p2[1]) >= 0 > (p1[0]-p2[0])-(p1[1]+p2[1]) or (p2[0]-p1[0])+(p2[1]+p1[1]) >= 0 > (p2[0]-p1[0])-(p2[1]+p1[1]):
            concounter += 0
        else:
            concounter += 1
            noncon.append([p1,p2])
        if (p1[0]-p3[0])+(p1[1]+p3[1]) >= 0 > (p1[0]-p3[0])-(p1[1]+p3[1]) or (p3[0]-p1[0])+(p3[1]+p1[1]) >= 0 > (p3[0]-p1[0])-(p3[1]+p1[1]):
            concounter += 0
        else:
            concounter += 1
            noncon.append([p1,p3])
        if (p2[0]-p3[0])+(p2[1]+p3[1]) >= 0 > (p2[0]-p3[0])-(p2[1]+p3[1]) or (p3[0]-p2[0])+(p3[1]+p2[1]) >= 0 > (p3[0]-p2[0])-(p3[1]+p2[1]):
            concounter += 0
        else:
            concounter += 1
            noncon.append([p2,p3])
        if (p1[0]-p4[0])+(p1[1]+p4[1]) >= 0 > (p1[0]-p4[0])-(p1[1]+p4[1]) or (p4[0]-p1[0])+(p4[1]+p1[1]) >= 0 > (p4[0]-p1[0])-(p4[1]+p1[1]):
            concounter += 0
        else:
            concounter += 1
            noncon.append([p1,p4])
        if (p2[0]-p4[0])+(p2[1]+p4[1]) >= 0 > (p2[0]-p4[0])-(p2[1]+p4[1]) or (p4[0]-p2[0])+(p4[1]+p2[1]) >= 0 > (p4[0]-p2[0])-(p4[1]+p2[1]):
            concounter += 0
        else:
            concounter += 1
            noncon.append([p2,p4])

    #Calculation of the solution:
        print("Concounter=",concounter)
        print("Glucose/v1",self.v1)
        print("Lactate/v4",self.v4)
        print("v5",self.v5)
        print("v6",self.v6)
        print("v7",self.v7)
        print("Nonconform pairs:",noncon)
        print("2v1-v4-v5 = 0 | {} +- {}".format((p1[0]-p2[0]),(p1[1]+p2[1])))
        print("2v1-v4-2v6 = 0 | {} +- {}".format((p1[0]-p3[0]),(p1[1]+p3[1])))
        print("v5-2v6 = 0 | {} +- {}".format((p2[0]-p3[0]),(p2[1]+p3[1])))
        print("2v1-v4-2v7 = 0 | {} +- {}".format((p1[0]-p4[0]),(p1[1]+p4[1])))
        print("v5-2v7 = 0 | {} +- {}".format((p2[0]-p4[0]),(p2[1]+p4[1])))
        print("v6-v7 = 0 | {} +- {}".format((self.v6 - self.v7),(self.v6*0.05 + self.v7*0.05)))    
        #return

             
    ######
    # functions that create widgets
    #
    #
    #
    ###
    
    def build_init_display(self):
        StudID = widgets.IntText( description='Student ID:', value=0 )
        button_StudID   = widgets.Button( description='Generate Parameters' )
        output = widgets.Output()

        disp=widgets.VBox([StudID,button_StudID, output]) 
        return disp
    
###############
###############
###############
    def build_question_display(self):
            listofwidgets = []

            # build question label/output (top 0)
            # build 'Get help button' (top 1)
            # build output (for commentsof help button) (top 2)
            listofwidgets.append(widgets.Output())

            listofwidgets.append(widgets.Button(
                value=False,
                description='Calculation Help',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltip='Click to get a tipp',
            #     icon='check' # (FontAwesome names without the `fa-` prefix)
            ))

            listofwidgets.append(widgets.Output())

            disp = widgets.VBox(listofwidgets)
            return disp
    
    ######
    # ON-CLICK functions
    # 2 per question
    #
    #
    ###
    def on_init_homework_button_clicked(self, click):
        self.init_display.children[1].disabled = True
        StdID = self.init_display.children[0].value
        self.start_homework(StdID)
    
    def on_question_one_help_button_clicked(self, click):
        self.hq1tgl = 1
        self.question_one_display.children[1].disabled = True
        with self.question_one_display.children[-1]:
            txt = """
##########\n
The task is to establish the independent balances of the stoichiometric matrix G:\n\n
* First step is to establish all balances for the six intracellular metabolites.\nThis is also described in the scripts 'Stoichiometric models I' p. 18.\n\n
* Second step is the gaussian elimination of the converted matrix\nThis is also described in the scripts 'Stoichiometric models I' p. 20-21.\n\n
The number of independent balances can be read off from there.\n
##########\n
            """#HHAVE TO HAVE ANOTHE RLOOK AT THIS
            print(txt)
        
    def on_question_two_help_button_clicked(self, click):
        self.hq2tgl = 1
        self.question_two_display.children[1].disabled = True
        with self.question_two_display.children[-1]:
            txt = """
##########\n
This task is to determine if the observed flux values are consistent or not.\nFor this scenario, consistency is proven when all established dependent relationships\nare consistent with the observed metabolic flux-rates\n\n
* Calculate the standard deviation for all experimental flux rates
* In Question 1, you have calculated the interdepencies of the flux equations of the stoichiometric matrix\nuse these established relationships between fluxes to determine\nif they are consistent to each other.
* If you find a pair of dependent fluxes that are not consistent to one another, the system itself can’t be consistent.\n
Example:\nv_Acetate - v_Ethanol = 0 |  (5.0 - 5.5) +/- (0.25 + 0.275) = 0\n 
##########\n
            """#HHAVE TO HAVE ANOTHE RLOOK AT THIS
            print(txt)
            
##########
##########
##########
#class for homework 7
##########
##########
##########
class create_question_homework_seven():
    #Innit: a question is comprised of the actual
    #Question (string)
    #and a list of answer_options (string) and an int if they are true (1) or not (0)
    def __init__(self, question = str, answers = [], image = None):
        if image != None:
            try:
                file = open(image, "rb")
                image = file.read()
                self.image_widget = self.create_image_widget(image)
            except:
                print("No image to load!")
                self.image_widget = None
        else:
            self.image_widget = None
        self.question = question
        self.answerobjects = []
        self.create_answer_option_objects(answers)
        #self.answerobjects = self.create_answer_option_objects()
        #self.answerobjects2 = []
        
    #create a label with the question
    def create_question_label(self):
        self.question_label  = widgets.Label(value=self.question)
        return
    
    def create__verify_button(self):
        self.verify_button = widgets.Button(
            description='Verify answer',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click here to verify your answer!',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        return
    
    def create_image_widget(self, image):
        i =  widgets.Image(
            value=image,
            format='png',
            width=300,
            height=300,
        )
        return i
    
    #def create_answer_option_objects(self):
    #    list_of_objects = []
    #    for i in self.answers:
    #        y = create_answer_option(i[0],i[1])
    #        list_of_objects.append(y)
    #    return list_of_objects
    
    def create_answer_option_objects(self, original_list_of_answers):
        list_of_answers = copy.deepcopy(original_list_of_answers)
        x = len(list_of_answers)
        if x == 1:
            self.answerobjects.append(create_answer_option(list_of_answers[0]))
            return
        if x == 0:
            print('Something went wrong')
            return
        else:
            y = rd.randint(0,x-1)
            self.answerobjects.append(create_answer_option(list_of_answers[y]))
            del list_of_answers[y]
            self.create_answer_option_objects(list_of_answers)
            return
    
    def check_answer_option_objects(self):
        for i in self.answerobjects:
            i.check_anwer_option()
        return
    
    def get_full_question(self):
        l = []
        self.create_question_label()
        self.create__verify_button()
        l.append(self.question_label)
        
        if self.image_widget != None:
            l.append(self.image_widget)
        
        for i in self.answerobjects:
            l.append(i.button)
        
        l.append(self.verify_button)
        wbox = widgets.VBox(l)
        return wbox
    
    def on_button_clicked(self, click):
        self.verify_button.disabled = True
        self.check_answer_option_objects()

class create_answer_option():
    #this takes the list of answer options of a question and turns it into toogle.button widgets
    #Position 0 in the list is the descripion
    #Position 1 in the list is if the answer option is True(1) or false (0)
    #Position 2 in the list is for the case that it's not a True-False question.
        #this is why len(inputlist) is checked
        
    #Note: this is backwards and should be exchanged through a *args but the def calling these
    # create_answer_option objects needs to call the positions in the greater list/dict, so that isnt possible (YET)
    def __init__(self, inputlist):
        self.descr = inputlist[0]
        self.yesorno = inputlist[1]
        
        if len(inputlist) == 3:
            optionlist = inputlist[2]
        else:
            optionlist = [("True",1),("False",0)]
        
        self.optionlist = optionlist
        self.button = self.create_answer_option_button()

    #create a toggle button for a single answer_option
    def create_answer_option_button(self):
        w = widgets.ToggleButtons(
            options= self.optionlist,
            description=self.descr,
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
           # tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
        return w
    
    def check_anwer_option(self):
        if self.button.value == self.yesorno:
            if self.button.value == 1:
                self.button.icons = ["check",""]
            if self.button.value == 0:
                self.button.icons = ["","check"]
            self.button.button_style = 'success'
            self.button.disabled = True
        elif self.button.value != self.yesorno:
            if self.button.value == 1:
                self.button.icons = ["","check"]
            if self.button.value == 0:
                self.button.icons = ["check",""]
            self.button.button_style = "danger"
            self.button.disabled = True

##########
##########
##########            
class create_homework_seven_task():
    def __init__(self, question, solution):
        self.question = question
        self.sol = solution
        self.create_int_text()
        self.create_question_label()
        
    def create_question_label(self):
        self.question_label = widgets.Label(
            value=self.question,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto')    
        )
    
    def create_int_text(self):
        self.int_text = widgets.IntText(
            value=0,
            description='Answer:',
            tooltip ='Answer:',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
    
    def create_verify_button(self):
        self.verify_button = widgets.Button(
            description='Verify answer',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click here to verify your answer!',
            icon='check', # (FontAwesome names without the `fa-` prefix),
            display='flex',
            align_items='center',
            flex_flow='column',
            #align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='50%', height='40px')
        )
        
    def on_verify_button_clicked(self, click):
        if self.int_text.value == self.sol:
            self.verify_button.disabled = True
            self.int_text.disabled = True
            self.verify_button.button_style = 'success'
            self.verify_button.description="Correct answer!"
        else:
            #self.verify_button.disabled = True
            #self.int_text.disabled = True
            self.verify_button.button_style = 'danger'
            self.verify_button.description="Wrong answer. Please try again!"
            
    def get_full_question(self):
        self.create_verify_button()
        #self.create_help_button()
        #i = [self.verify_button, self.help_button]
        #hbox = widgets.HBox(i)
        
        j = [self.question_label, self.int_text,self.verify_button]
        wbox = widgets.VBox(j)
        return wbox
##########
##########
##########
class create_homework_seven_task_one_one():
    def __init__(self, matricnb = int):
        self.init_display = self.build_init_display()
        self.question =  "What is the maximum specific growth rate? [1/h]"
        #self.create_solution() #needs self.ID from self.init_display #gets moved to on-click event in init-display
        self.create_float_text()
        self.create_question_label()
        self.output = widgets.Output()
        #self.ID created by on-click event on button in self.init_display
        #self.sol created by  self.create_solution()
    
    def create_solution(self, ID):
        if type(ID) == int:
            rd.seed(ID)
            listofrndms = [rd.random() for i in range(10)]
            #self.sol = 0.300+listofrndms[9]*0.100
            self.sol = 0.386
        elif matricnb == "Test":
            self.sol = 0.386
        else:
            with self.init_display.children[-1]:
                print("matriculation number has to be an integer!")
                #self.output.clear_output(wait=True)
    
    def create_question_label(self):
        self.question_label = widgets.Label(
            value=self.question,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto')    
        )
    
    def create_float_text(self):
        # create two Float-TExt widgets that get implemented into the question interface
        # self.float_corr is the correlation coefficient R
        # self.float_mue is the growth rate µ
        # both user-inputs can be checked by taking the value in 'widget'.value
        self.float_corr = widgets.FloatText(
            value=0,
            description='Correlation Coefficient\n|| Example: R^2 = 0.00 (Float)',
            tooltip ='Correlation Coefficient\n|| Example: R^2 = 0.00 (Float)',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
        self.float_mue = widgets.FloatText(
            value=0,
            description='maximum specific growthrate\n|| Example: µ = 1.00 (Float)',
            tooltip ='maximum specific growthrate\n|| Example: µ = 1.00 (Float)',
            disabled=False,
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
    
    def create_verify_button(self):
        self.verify_button = widgets.Button(
            description='Verify answer',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click here to verify your answer!',
            icon='check', # (FontAwesome names without the `fa-` prefix),
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
            
    def create_help_button(self):
        self.help_button = widgets.Button(
            description='Help required?',
            disabled=False,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click here to get a tipp!',
            display='flex',
            flex_flow='column',
            align_items='stretch',
            style= {'description_width': 'initial'},
            layout = widgets.Layout(width='auto', height='40px')
        )
        
    def on_verify_button_clicked(self, click):
        self.verify_button.button_style = 'warning'
        self.verify_button.description="Wrong answer. Please try again!"
        #First step: Check if correlation coefficient is > 0.95
        #If yes: move on to growth-rate
        #if no: depict on verify button and return
        if self.float_corr.value > 1.00:
            self.verify_button.button_style = 'warning'
            self.verify_button.description="Correlation Coefficient can't be > 1.00. Please try again!"
        elif 0.95 <= self.float_corr.value <= 1.00:
        #Second Step: check if growth rate solution is correct (is equal to self.sol) 
        #If yes: answer correct
        #If no: Answer wrong
        #If close to correc: depict on verify button
            if round(self.float_mue.value,2) == round(self.sol,2):
                self.verify_button.disabled = True
                self.float_corr.disabled = True
                self.float_mue.disabled = True
                self.verify_button.button_style = 'success'
                self.verify_button.description="Correct answer!"
                return
            elif round(self.float_mue.value,1) == round(self.sol,1):
                self.verify_button.button_style = 'danger'
                self.verify_button.description="Wrong answer, but close! Please try again!"
                return
        else:
            self.verify_button.button_style = 'warning'
            self.verify_button.description="Correlation Coefficient has to be > 0.95. Please try again!"
                
            
    def on_help_button_clicked(self, click):
        self.help_button.disabled = True
        txt = """
##########\n
For cells growing at a constant specific growth rate µ, the biomass concentration x increases with time:\n
x_i = x_0 * e^m\n
µ can be determined by plotting the natural logarithm of the OD against the time h\nand determining the slop of the exponential growth phase\n 
µ = (ln(x_o) - ln(x_i)) / t\n\n
Note:\n
* To assume a linear correlation between µ and t, atleast three data points are required\n
* The correlation coefficient R^2 has to be > 0.95 
##########\n
        """
        with self.output:
            print(txt)
            
    #on-click in init-display:
    #store Student-ID in self.ID
    def on_init_homework_button_clicked(self, click):
        self.init_display.children[1].disabled = True
        ID = self.init_display.children[0].value
        self.create_solution(ID)
        with self.init_display.children[2]:
            print("#####\nStudent-ID accepted!\nGood luck!\n#####")

    
    def get_full_question(self):
        self.create_verify_button()
        self.create_help_button()
        i = [self.verify_button, self.help_button]
        hbox = widgets.HBox(i)
        
        j = [self.question_label, self.float_corr, self.float_mue, hbox, self.output]
        wbox = widgets.VBox(j)
        return wbox
    
    def build_init_display(self):
        StudID = widgets.IntText( description='Student ID:', value=0 )
        button_StudID   = widgets.Button( description='Generate Parameters' )
        output = widgets.Output()

        disp=widgets.VBox([StudID,button_StudID, output]) 
        return disp

###
def full_question_objects():
    q_1_1_answers = [
        ["for butanol between 17 h - 32 h from the start of the process",0],
        ["for neither butanol or butyrate",0],
        ["for butyrate between 8 h - 14 h from the start of the process",1]    
    ]
    q_1_2_answers = [
        ["is reached after complete glucose degradiation",0],
        ["is 18.4 mM/h",1],
        ["is reached before complete butyrate degradiation",1],
        ["is 13.3 mM/h",0]
    ]
    q_1_3_1_answers = [
        ["increases linearly",0],
        ["decreeases linearly",0],
        ["increases exponentially",1],
        ["decreases exponentially",0],
        ["stays constant",0]
    ]
    q_1_3_2_answers = [
        ["stays the same",0],
        ["exponentially",1],
        ["linearly",0]
    ]
    q_1_3_3_answers = [
        ["a linear increase in product concentration",0],
        ["an exponential increase in product concentration",1]
    ]
    q_1_3_4_answers = [
        ["the kinetic orders of both formation processes are the same",1],
        ["the formation rates of both formation processes are the same",0],
        ["product formation is growth-dependent",1],
        ["product formation is growth-independent",0]
    ]
    q_2_1_answers = [
        ["1+2 are organic solvents",0],
        ["3+4 are organic solvents",1],
        ["1+2 are organic acids",1],
        ["3+4 are organic acids",0]
    ]
    q_2_2_answers = [
        ["Acetyl-CoA ↔ Acetat + ATP\nAcetoacetyl-CoA + Butyrat → Aceton + CO2 + Butyryl-CoA",0],
        ["Butyryl-CoA ↔ Butyrat + ATP\nAcetoacetyl-CoA + Acetat → Aceton + CO2 + Acetyl-CoA",0],
        ["Butyryl-CoA ↔ Butyrat + ATP\nAcetoacetyl-CoA + Butyrat → Aceton + CO2 + Butyryl-CoA",1],
        ["Acetate_extracellular ↔ Acetate_intracellular\nAcetoacetyl-CoA + Acetat → Aceton + CO2 + Acetyl-CoA",1],
        ["Acetyl-CoA ↔ Acetat + ATP\nAcetoacetyl-CoA + Acetat → Aceton + CO2 + Acetyl-CoA",1]
    ]
    q_2_3_1_answers = [
        ["not be determined by determining the concentration over time using HPLC,\nsince the metabolic network has too many degrees of freedom (is underdetermined).",1],
        ["be determined by determining the concentration over time using HPLC.",0],
        ["not be determined by determining concentration over time using HPLC since acetone is volatile.",0]
    ]
    q_2_3_2_answers = [
        ["undetermined; not all intracellular rates can be calculated.",1],
        ["over-determined; all intracellular rates can be calculated and error estimation performed.",0],
        ["determined; all intracellular rates can be determined.",0]
    ]
    q_3_1_answers = [
        ["Acetyl-CoA ↔ Acetat + ATP\nAcetoacetyl-CoA + Acetat → Aceton + CO2 + Acetyl-CoA",0],
        ["Butyryl-CoA ↔ Butyrat + ATP",1],
        ["Acetoacetyl-CoA → Acceton + CO2 + ATP",1],#added Aceton on Product side (Quant-MiBi_Calc-Guide.pdf, p. 30)
        ["Acetyl-P ↔ Acetat + ATP",0],
        ["Butyryl-CoA ↔ Butyrat + ATP\nAcetoacetyl-CoA + Butyrat → Aceton + CO2 + Butyryl-CoA",0],
        ["Acetyl-CoA ↔ Acetat + ATP",1]
    ]
    q_3_2_answers = [
        ["",0,[("Yes",1),("No",0)]]
    ]
    question_dict = {}
    question_dict["q_1_1"] = ["The formation is directly proportional to the biomass increase:",q_1_1_answers, None]
    question_dict["q_1_2"] = ["The maximum rate of butanol formation:",q_1_2_answers, None]
    question_dict["q_1_3_1"] = ["If the biomass concentration increases exponentially over time, the biomass formation rate is:",q_1_3_1_answers, None]
    question_dict["q_1_3_2"] = ["For cells that proliferate at a constant specific growth rate µ, the concentration of biomass increases over time:",q_1_3_2_answers, None]
    question_dict["q_1_3_3"] = ["Product formation according to first-order kinetics corresponds to:",q_1_3_3_answers, None]
    question_dict["q_1_3_4"] = ["If there is a linear relationship between the product and biomass concentration r_x:",q_1_3_4_answers, None]
    question_dict["q_2_1"] = ["Which C. acetobutylicum products are represented by curves 1, 2, 3, and 4?",q_2_1_answers, "data/801059_Graph_Blank1997_Prozess_C_acetobutylicum_lora_080703_v3_modified4question.png"]
    question_dict["q_2_2"] = ["Which reaction equations represent a possible synthetic route to acetone?",q_2_2_answers, None]
    question_dict["q_2_3_1"] = ["The reaction rates to acetone can:",q_2_3_1_answers, None]
    question_dict["q_2_3_2"] = ["The metabolic (stoichiometric) model is:",q_2_3_2_answers, None]
    question_dict["q_3_1"] = ["Which reaction equations represent the net equations for butyrate, acetate and acetone?",q_3_1_answers, None]
    question_dict["q_3_2"] = ["Is the acetone synthesis rate determinable?",q_3_2_answers, None]
    
    
    list_of_objects = []
    for i in question_dict.keys():
        list_of_objects.append(create_question_homework_seven(question_dict[i][0],question_dict[i][1], question_dict[i][2]))
    return list_of_objects

def full_task_objects():
    #t_1_1 = [
    #    "What is the maximum specific growth rate? [1/h]",0.368
    #]
    t_2_1_1 = [
        "How many reaction rates does the stoichiometric model representing the metabolic network of C. acetobutylicum contain?",20
    ]
    t_2_1_2 = [
     "How many reaction pathways are there for the synthesis of acetone in C. acetobutylicum?",2   
    ]
    t_2_2_1 = [
     "How many rates are in r_m?",8
    ]
    t_2_2_2 = [
     "The number of rates r_c to calculate is:",12#is 12 correct?   
    ]
    t_2_2_3 = [
     "How many of (all) the rates can be determined using liquid chromatography (HPLC with any detector) and a spectrophotometer?",8   
    ]
    t_3_1 = [
     "How many reaction equations does the simplified metabolic model for calculating the intracellular reaction rates including acetone production contain?",11   
    ]

    task_dict = {}
    #task_dict["t_1_1"] = t_1_1 #NOTE: Task 1.1 requires calculation and a float value as answer. because of this, it was kept seperate.
    task_dict["t_2_1_1"] = t_2_1_1
    task_dict["t_2_1_2"] = t_2_1_2
    task_dict["t_2_2_1"] = t_2_2_1
    task_dict["t_2_2_2"] = t_2_2_2
    task_dict["t_2_2_3"] = t_2_2_3
    task_dict["t_3_1"] = t_3_1
    
    
    list_of_objects = []
    for i in task_dict.keys():
        list_of_objects.append(create_homework_seven_task(task_dict[i][0],task_dict[i][1]))
    return list_of_objects