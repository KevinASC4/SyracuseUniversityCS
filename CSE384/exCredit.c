#include <stdio.h>
#include<stdlib.h>
// fig06_17.c
// Two-dimensional array manipulations.
#include <stdio.h>
#define STUDENTS 3
#define EXAMS 4

// function prototypes
void minimum(int grades[][EXAMS], size_t pupils, size_t tests);
void maximum(int grades[][EXAMS], size_t pupils, size_t tests);
void average(int grades[][EXAMS], size_t pupils, size_t tests);
void printArray(int grades[][EXAMS], size_t pupils, size_t tests);
void enterStudentGrades(int grades[][EXAMS], size_t pupils, size_t tests);
void (*processGrades[5]) (int grades[][EXAMS], size_t pupils, size_t tests) ={enterStudentGrades, printArray, minimum, maximum, average};

// function main begins program execution
int main(void) {
   // initialize student grades for three students (rows)
   int studentGrades[STUDENTS][EXAMS] =  
      {{0, 0, 0, 0},
       {0, 0, 0, 0},
       {0, 0, 0, 0}};
	int programRunning=6;
	while(programRunning!=5){
		printf("\n0\t Enter Grades\n");
		printf("1\t Print the array of Grades\n");
		printf("2\t Find the Minimum Grade\n");
		printf("3\t Find the Maximum Grade\n");
		printf("4\t Print the average on all tests for each student\n");
		printf("5\t End the Program\n");
		scanf("%d", &programRunning);
		if (programRunning == 0){
			(*processGrades[0])(studentGrades,STUDENTS,EXAMS);
		}if (programRunning == 1){
			(*processGrades[1])(studentGrades,STUDENTS,EXAMS);
		}if (programRunning == 2){
			(*processGrades[2])(studentGrades,STUDENTS,EXAMS);
		}if (programRunning == 3){
			(*processGrades[3])(studentGrades,STUDENTS,EXAMS);
		}if (programRunning == 4){
			(*processGrades[4])(studentGrades,STUDENTS,EXAMS);
		}
	}	
	return 0;
} 

// Find the minimum grade
void minimum(int grades[][EXAMS], size_t pupils, size_t tests) {
   int lowGrade = 100; // initialize to highest possible grade

   // loop through rows of grades
   for (size_t row = 0; row < pupils; ++row) {
      // loop through columns of grades
      for (size_t column = 0; column < tests; ++column) {
         if (grades[row][column] < lowGrade) {
            lowGrade = grades[row][column];
         } 
      } 
   } 

   printf("\nLowest Grade: %d\n",lowGrade); // return minimum grade 
} 

// Find the maximum grade
void maximum(int grades[][EXAMS], size_t pupils, size_t tests) {
   int highGrade = 0; // initialize to lowest possible grade

   // loop through rows of grades
   for (size_t row = 0; row < pupils; ++row) {
      // loop through columns of grades
      for (size_t column = 0; column < tests; ++column) {
         if (grades[row][column] > highGrade) {
            highGrade = grades[row][column];
         } 
      } 
   } 

   printf("\nHighest Grade: %d\n", highGrade); // return maximum grade
} 

// Determine the average grade for a particular student
void average(int grades[][EXAMS], size_t pupils, size_t tests) {     
	int totalGrade = 0;
	for (int student=0;student<STUDENTS; student++){
		for(int grade =0;grade<EXAMS;grade++){
			totalGrade += grades[student][grade];
		}
	}
	double averageGrade = totalGrade / (STUDENTS*EXAMS);
	printf("\nAverage Grade is: %f\n",averageGrade);
}

// Print the array
void printArray(int grades[][EXAMS], size_t pupils, size_t tests) {
   // output column heads
   printf("%s", "                 [0]  [1]  [2]  [3]");

   // output grades in tabular format
   for (size_t row = 0; row < pupils; ++row) {
      // output label for row
      printf("\nstudentGrades[%zu] ", row);

      // output grades for one student
      for (size_t column = 0; column < tests; ++column) {
         printf("%-5d", grades[row][column]);
      } 
   }
   
}
void enterStudentGrades(int grades[][EXAMS], size_t pupils, size_t tests){
	int studentID = 1;
	while(studentID){
	printf("Enter Student ID(1-3), 0 to exit\n");
	scanf("%d", &studentID);
	if (studentID!=0){
		for(int i=0;i<4;i++){
			int examNumber=i+1;
			printf("Enter Grade for exam %d: ",examNumber);
			scanf("%d", &grades[studentID-1][i]);
		}
	}
	else{
		break;
	}
	
	}
								
				
			
}
