"""
    This class is designed for consolidated result analysis for a group of students.
    It takes input data from an Excel file, processes it, calculates various statistics,
    and generates reports in the form of an Excel file and a PDF document.

    Parameters:
    
    - File_Path (str): The path to the input Excel file containing student data.
    - Sub_Code (list): List of subject codes.
    - Sub_name (list): List of subject names.
    - EX_Usn (str): A common prefix for USN (University Serial Number) to be stripped from student USNs.
    - Teacher_name (list): List of teacher names for each subject.

    Methods:

    - greatest(): Calculate the maximum marks, student counts, and USNs for each subject.
    - upend(): Append data to an Excel sheet.
    - count(num): Count the occurrences of elements in a list.
    - std(): Calculate and append statistics to the Excel sheet.
    - per(): Calculate percentages, total marks, and grades for students.
    - SGPA(student_marks): Calculate SGPA for a list of student marks.
    - something(): Perform additional calculations.
    - newsheet(): Generate a new Excel sheet with summary data.
    - F(): Find students who failed.
    - subtract(): Calculate the number of students who attempted each subject.
    - create_pdf_report(filename): Generate a PDF report with analysis results.

    Attributes:

    - lk (list): List of subject names.
    - path_in (str): Path to the input Excel file.
    - sub (list): List of subject codes.
    - path_out (str): Path to the output Excel file.
    - filename (str): Name of the PDF report file.
    - Teach_name (list): List of teacher names for each subject.
    - percentage (list): List of percentages for each student.
    - Total (list): List of total marks for each student.
    - marks_list (list): List of marks for each subject for each student.
    - Final (list): List of final results for each subject.
    - num (list): List of student counts for each subject.
    - gsa (list): Unused attribute.
    - grade (list): List of grades for each student.
    - o (list): Unused attribute.
    - x (DataFrame): Pandas DataFrame containing input data.
    - name (list): List of student names.
    - USN (list): List of student USNs.
    - python (list): List of Python subject marks for each student.
    - math (list): List of Math subject marks for each student.
    - civil (list): List of Civil subject marks for each student.
    - cad (list): List of CAD subject marks for each student.
    - chemistry (list): List of Chemistry subject marks for each student.
    - l (list): List of lists containing marks for each subject.
    - strength (list): List of the number of students in each subject.
    - dv (list): List of maximum marks for each subject.
    - dk (list): List of comma-separated USNs for students who scored maximum marks in each subject.
    - nm (list): List of comma-separated student names for students who scored maximum marks in each subject.

    Example Usage:
    
    File_Path=r"D:\\project\\c.xlsx"            
    Sub_Code=["21CS42(4)","21CS43(4)","21CS44(3)","21MATCS41(3)","21BE45(2)","21CS482(1)","21CSL46(1)","21CIP47(1)","21UH49(1)","21INT49(1)"]
    Sub_name=["Design Analysis",
    "Microcontroller and Embedded sysytem","Operating System","Mathematical Foundation of Computing","Biology for Engineers ","Unix shell Programming","Python Programming Lab","Indian Constitution","Universal Human Values","int49- internship"] 
    cradite=[4,4,3,3,2,1,1,1,1,1]   #111   
    Ex_Uns="1AH21CS"                        
    Teacher_name=["Mrs. Aswini","Mrs.vigneshwari","Mrs. Sandya Rani","Mr.Abishek ","Mr.Venkatesh kumar ","Dr.Senthil kuman","Mrs. Bhavani","Mrs. Shruthi","Dr.Pillai","Mr. Panchaxari"
        ]
    text=r"Consolidated Result Analysis for the Academic Year 2022-23 (Before Revaluation) 4‘a&b’ Semester."
    k=Result_cal(File_Path,Sub_name,Sub_Code,Ex_Uns,Teacher_name,cradite,text)    

    Install vs code nad download the following modules :
        1) pandas 
        2) openpyxl
        3) matplotlib

    Made by Tanishq JM CSE ACS College of Engineering
"""

try:
    from sys import *
    from pandas import *
    import openpyxl as op
except Exception as ex:
    print(        """
        Try the following command : -
        1) pip install pandas 
        2) pip install openpyxl
        3) pip install matplotlib
                """       ,ex          )

def output(path):
    if ".xlsx" in path:
        p=path.rstrip(".xlsx") 
        pd=p+"sample_report.pdf"
        p+="_output.xlsx"
        return(pd,p)
    pass

def count(num):
        op=[" "," "," "]
        uniqDig = set(num)
        for elem in uniqDig:
            op.append(f"{elem} = {num.count(elem)}")
        op=" ".join(op)
        return op

class Result_cal:
    '''  Ƭ₳₦łꚃⷮꚕⷹq 0.0.7 '''        
    def __init__(self,File_Path,Sub_Code,Sub_name,Teacher_name,cradite,text) -> None:
        try:
            print(Result_cal.__doc__)
            self.text=text
            self.cradite=cradite
            self.lk=Sub_name;self.path_in=File_Path;self.sub=Sub_Code
            self.filename ,self.path_out=output(File_Path)
            self.percentage=[] 
            self.Teach_name=Teacher_name
            self.Total=[] 
            self.marks_list=[] 
            self.Final=[] 
            self.num,self.gsa=[],[] 
            self.grade=[];self.usn_of_max_marks=[]
            self.o=[" "," "]
            self.x=read_excel(self.path_in);self.name=[self.x["name"][i] for i in range(len(self.x['name']))] 
            self.USN=[self.x['usn'][i] for i in range(len(self.x['usn']))]#.lstrip(ud)
            self.baag=[]
            new=[]
            for k in range(len(self.sub)):
                new.append([ self.x[self.lk[k]][i] for i in range(len(self.x[self.lk[k]]))])
            self.l=new
            #[self.subject1,self.subject2,self.subject3,self.subject4,self.subject5,self.subject6,self.subject7,self.subject8,self.subject9,self.subject10]
            self.dv,self.dk,self.nm=self.greatest() 
            # print(self.dv,self.dk,self.nm)
            self.strength=[len(self.l[i]) for i in range(len(self.l))]
            self.fal=self.F() 
            self.subtract()
            self.something() 
            self.given_test_data=[len(self.l[i]) for i in range(len(self.l))]
            # print(self.strength,self.USN)     
            self.p=[sum(self.Final[i])-self.Final[i][3] for i in range(len(self.Final))]
            self.per2=[str(int(self.p[i]*100/self.given_test_data[i]))+"%" for i in range(len(self.Final))]
            self.newsheet()
   
        except Exception as ex:
            print(ex)
            exit
   
    def greatest(self):
   
        try:
            nm=[];dv=[];dk=[];du=[]
            for i in range(len(self.l)):
                keys=max(self.l[i])  
                temp=[];temo=[]  
                j=0
                for k in range(len(self.l[i])):
                    if keys==self.l[i][k]:
                        j+=1
                        temp.append(self.USN[k]);temo.append(self.name[k])      
                self.num.append(j)           
                dv.append(keys)         
                val=self.l[i].index(keys)
                dk.append(",".join(temp)) 
                nm.append(",".join(temo))
            for i in range(len(dk)):
                k=dk[i].split(',')
                du.append(k[-1])
                pass
            return dv,du,nm

        except Exception as ex:
            print(ex)
            exit

    def per(self):

        try:
            for i in range(len(self.USN)):       
                        sum=0;makes=[]
                        for k in range(len(self.l)):
                            sum+=self.l[k][i]
                            makes.append(self.l[k][i])
                        self.percentage.append(sum/len(self.l))
                        self.Total.append(sum)
                        self.marks_list.append(makes) #marks of each student ...
            cgpa=[self.SGPA(self.marks_list[i]) for i in range(len(self.marks_list))] # cgpa if needed ...
            for i in range(len(self.percentage)):   #grade counter which will be appended in to the grade >
                temp=self.percentage[i]
                if self.USN[i] in self.fal:
                    self.grade.append("F")
                elif temp>=70:
                    self.grade.append("FCD")
                elif temp<=69 and temp>=60:
                    self.grade.append("FC")
                elif temp<=59 and temp>=41:
                    self.grade.append("SC")
                else:
                    self.grade.append("F")
        except Exception as ex:
            print(ex)
            exit
            pass

    def SGPA(self,student_marks):

        try:
            grade=[];Total=0     
            for i in student_marks:
                Total+=i;q=(i//10)
                if q<10:
                    q+=1
                else:
                    pass
                grade.append(q)
            gxc=[];ct=0
            #Calculate the sgpa ...
            for i in range(len(self.cradite)): #8
                k=grade[i]*self.cradite[i]
                gxc.append(k)
                ct+=k
            sgpa=ct/20
            per=Total/len(self.cradite)
            return sgpa
        except Exception as ex:
            print(ex)
            exit

    def something(self):

        try:
            j=[]
            for k in range(len(self.l)):
                grade=[]
                for i in range(len(self.l[k])):
                        temp=self.l[k][i]
                        if temp>=70 and temp<=100:
                            grade.append("FCD")
                        elif temp<=69 and temp>=60:
                            grade.append("FC")
                        elif temp<=59 and temp>=41:
                            grade.append("SC")
                        else:
                            grade.append("F")
                j.append(grade)
                b=self.count(grade)
                self.o.append(b)
            for z in range(len(j)):
                q=[]
                fcd,fc,sc,f=0,0,0,0
                for t in range(len(j[z])):
                    temp=j[z][t]
                    if temp=="FCD":
                        fcd+=1
                    elif temp=="FC":
                        fc+=1
                    elif temp=="SC":
                        sc+=1
                    else:
                        f+=1
                q.append(fcd);q.append(fc);q.append(sc);q.append(f)
                self.Final.append(q)

        except Exception as ex:
            print(ex)
            exit

    def count(self,num):
        try:
            op=[" "," "," "]
            uniqDig = set(num)
            for elem in uniqDig:
                op.append(f"{elem} = {num.count(elem)}")
            op=" ".join(op)
            return op

        except Exception as ex:
            print(ex)
            exit

    def F(self):

        try:
            fal=[]
            for i in range(len(self.l)):
                for k in range(len(self.l[i])):
                    temp=self.l[i][k]
                    if temp<=40:
                        fal.append(self.USN[self.l[i].index(temp)])   
            return list(set(fal))

        except Exception as ex:
            print(ex)
            exit
    
    def subtract(self):
    
        try:
            temp = []
            for i in range(len(self.l)):
                k = []
                count = 0
                for t in range(len(self.l[i])):
                    if self.l[i][t] == -2:
                        self.l[i][t] = 0  
                        k.append(t)
                        count += 1
                self.baag.append(len(self.l[i]) - count)
                temp.append(k)
            self.per()
            for i in range(len(self.l)):
                for t in range(len(temp[i]) - 1, -1, -1):  
                    index_to_pop = temp[i][t]
                    if index_to_pop < len(self.l[i]):
                        lll = self.l[i].pop(index_to_pop)
                    else:
                        print("Index out of range : ", index_to_pop)
        
        except Exception as ex:
                print(ex)

    
    def newsheet(self):
        
        try:
            br=[];    q=[]
            fcd,fc,sc,f=0,0,0,0
            for t in range(len(self.grade)):
                temp=self.grade[t]
                if temp=="FCD":
                    fcd+=1
                elif temp=="FC":
                    fc+=1
                elif temp=="SC":
                    sc+=1
                else:
                    f+=1
            q.append(fcd);q.append(fc);q.append(sc);q.append(f);br.append(q) #Appending the data ...
            exp=self.Total.copy();exp.sort(reverse=True)
            top=[exp[i] for i in range(3)]
            w=sum(br[0])
            l=w-br[0][3]
            
            def create_pdf_report(filename):
            
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter, landscape
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle ,PageBreak
                from reportlab.lib.styles import getSampleStyleSheet
            
                doc = SimpleDocTemplate(self.filename, pagesize=landscape(letter))    # Create a list to hold the content of the PDF
                elements = []                                                    # Add a title to the PDF
                title_style = getSampleStyleSheet()["Title"]
                title = Paragraph("ACS COLLEGE OF ENGINEERING", title_style)
                elements.append(title);     elements.append(Spacer(1, 20))        # Add some spacing    # Add a paragraph of text
                text_style = getSampleStyleSheet()["Title"]
                text = Paragraph(self.text, text_style)
                elements.append(text);      elements.append(Spacer(1, 20))
                text_style = getSampleStyleSheet()["Title"]
                title = Paragraph("Department of Computer science",text_style)
                elements.append(title);     elements.append(Spacer(1, 10))
                data=[
                        ["Semester","4","","","Total number \n of \n students",len(self.USN),"Appeared",len(self.USN),"Over all"," "," ","Topper list"," "],
                        ["Faculty Name","Subject Code","Total","Attempted","Subject Name", "FCD","FC","SC","Fail","Pass","%"," ","marks"],]
                for i in range(len(self.lk)):
                    data.append([self.Teach_name[i],self.lk[i],self.strength[i],self.given_test_data[i],self.sub[i],self.Final[i][0],self.Final[i][1],self.Final[i][2],self.Final[i][3],self.p[i],self.per2[i],self.dk[i].split(',')[0],self.dv[i]])
                data.append([" "," "," "," "," "," "," "," "," "," "," Over Passed "])
                data.append([" "," "," "," "," "," "," "," "," "," Tot_stu",l,str((l*100//w))+"%"])
                data.append([" "," "," "," "," "," "," "," "," ","FCD",br[0][0],str(round((br[0][0]/max(self.given_test_data)*100)))+"%"])
                data.append([" "," "," "," "," "," "," "," "," ","FC",br[0][1],str(round((br[0][1]/max(self.given_test_data))*100))+"%"])
                data.append([" "," "," "," "," "," "," "," "," ","SC",br[0][2],str(round((br[0][2]/max(self.given_test_data)*100)))+"%"])
                data.append([" "," "," "," "," "," "," "," "," ","Fail",br[0][3],str(round((br[0][3]/max(self.given_test_data))*100))+"%"])
                data.append([" "," "," "," "," "," "," "," "," "," ","Toppers list"])
                data.append([" "," "," "," "," "," "," "," "," ",self.USN[self.Total.index(top[0])],self.name[self.Total.index(top[0])],top[0],self.percentage[self.Total.index(top[0])]])
                data.append([" "," "," "," "," "," "," "," "," ",self.USN[self.Total.index(top[1])],self.name[self.Total.index(top[1])],top[1],self.percentage[self.Total.index(top[1])]])
                data.append([" "," "," "," "," "," "," "," "," ",self.USN[self.Total.index(top[2])],self.name[self.Total.index(top[2])],top[2],self.percentage[self.Total.index(top[2])]])
                
                
                table = Table(data)
                table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])) #table_width = 300  # Set the desired width in points
            
                table_width = 100   # Set the desired width in points #table._argW[0] = table_width  # Update the width of the first column
                table._argW[0] = table_width 
                page_width, page_height = doc.pagesize
                extended_page_width = page_width + table_width  # Extend the page by the table width             # Update the page size
                if len(self.lk)<11:
                    extended_page_width *=1.15
                    page_height *=1.15
                
                doc.pagesize = (extended_page_width*1.5, page_height*1.5)
                elements.append(table)
                data=[[],[" "],[" "],[" "],["HOD",' ',' ',' ',' ',' ','','','','','','','','','','','','','','','','','','','','','','','','','','',
                    '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','Principle']]
                table = Table(data)
                table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('FONTNAME', (0, 1), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 18),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.white)]))
                elements.append(table)
                doc.build(elements)
            
            
            create_pdf_report(self.filename)
            
            try:
                def graph():
                    import matplotlib.pyplot as plt
                    subjects = ['FCD', 'FC', 'SC', 'F']
                    marks = [br[0][0],br[0][1],br[0][2],br[0][3]]  
                    colors = ['gold', 'lightblue', 'lightgreen', 'lightcoral']
                    explode = (0.1, 0, 0, 0)  
                    plt.figure(figsize=(8, 6))
                    patches, texts, autotexts = plt.pie(marks, labels=subjects, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
                    plt.title('Result Analysis - Subjects')
                    for text in texts:
                        text.set_color('black')  
                    for autotext in autotexts:
                        autotext.set_color('black')
                        autotext.set_fontsize(10)  
                    plt.legend(patches, subjects, loc="best")
                    plt.axis('equal')  
                    plt.savefig('result_analysis_pie_chart.png', bbox_inches='tight')  # Save with tight bounding box
                    plt.show()
                    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
                    plt.title("Subject_Result")
                    axs[0].bar(self.lk, self.strength, color='blue')
                    axs[0].set_ylabel('Total Students')
                    axs[1].bar(self.lk, self.given_test_data, color='orange')
                    axs[1].set_ylabel('Attempted Students')
                    axs[2].bar(self.lk, self.p, color='green')
                    axs[2].set_ylabel('Passing Students')
                    plt.tight_layout()
                    plt.savefig('Student_subject_result.png') # Save 


            except Exception as ex:
                print("Graph creating error : ",ex)
                exit()
            graph()


        except Exception as ex:
            print("Pdf creating error : ",ex)
            exit()


# Example...
"""File_Path=r"D:\\project\\c.xlsx"            

Sub_Code=["21CS42(4)"
,"21CS43(4)",
"21CS44(3)"
,"21MATCS41(3)"
,"21BE45(2)",
"21CS482(1)"
,"21CSL46(1)"
,"21CIP47(1)"
,"21UH49(1)",
"21INT49(1)"]

Sub_name=["Design Analysis",

"Microcontroller and Embedded sysytem",
"Operating System",
"Mathematical Foundation of Computing"
,"Biology for Engineers "
,"Unix shell Programming",
"Python Programming Lab"
,"Indian Constitution"
,"Universal Human Values"
,"int49- internship"] 

cradite=[4,4,3,3,2,1,1,1,1,1]   #111   

Teacher_name=[
"Mrs. Aswini",
"Mrs.vigneshwari",
"Mrs. Sandya Rani",
"Mr.Abishek ",
"Mr.Venkatesh kumar ",
"Dr.Senthil kuman",
"Mrs. Bhavani",
"Mrs. Shruthi",
"Dr.Pillai",
"Mr. Panchaxari"
]

text=r"Consolidated Result Analysis for the Academic Year 2022-23 (Before Revaluation) 4‘a&b’ Semester."

k=Result_cal(File_Path,Sub_name,Sub_Code,Teacher_name,cradite,text)    """ 

"Line number 500 ....  "