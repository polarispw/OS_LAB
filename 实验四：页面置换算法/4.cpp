#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <error.h>
#include <wait.h>
#include <time.h>
#include <unistd.h>

#define true 1
#define false 0
#define frame_num 3
#define frame_num_FIFO 4
#define sequence_len 12

typedef enum { USED, UNUSED }frame_flag;/* flag of frame */

typedef struct oneframe { 
	int page_no; 
    frame_flag flag; 
}one_frame;

int main()
{
	/***********initialize variable***********/
	int i, j, pid, gtid, reid;
	int access_index = 0;		       		 // the index of Access_Series
	int success_flag = false;	       		 // value is true if page exists 
	float diseffect = 0.0;		       		 // pages absence counts 
	float absence_rate = 0.0;	      		 // absence_rate = diseffect / sequence_len 
	float success_rate = 0.0;	      		 // success_rate = 1 - absence_rate 
    int Access_Series[sequence_len]; 	 // random number sequence 
    one_frame M_Frame[frame_num];  	     	 // memory access sequence 
	one_frame M_Frame_FIFO[frame_num_FIFO];  // memory access sequence FIFO
	int Belady[sequence_len] = {1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5}; // Belady
	
	/***********initialize memory access series***********/
	printf("Do you want to see Belady? (1-yes  2-no)\n");
	do{
		printf("Your choice: ");
		scanf("%d", &i);
	}while(i != 1 && i != 2);
	if(i == 1)
	{
		for(int k = 0; k < sequence_len; k++)
		{
			Access_Series[k] = Belady[k];
			printf("%d ",Access_Series[k]);	
		}
	}
	else if(i == 2)
	{
		srand((int)time(0));		       		 
		printf("\n* access series numbers:");
		for(int k = 0; k < sequence_len; k++)
		{	
			Access_Series[k] = 1 + (int)(10.0 * rand() / (RAND_MAX + 1.0));	//[1,10]
			printf("%d ",Access_Series[k]);	
		}
	}
	printf("\n\n");

	/***********initialize data structure M_Frame***********/
    for(i = 0; i < frame_num; i++)
	{	
		M_Frame[i].page_no = 0;
		M_Frame[i].flag = UNUSED;
	}

	for(i = 0; i < frame_num_FIFO; i++)
	{	
		M_Frame_FIFO[i].page_no = 0;
		M_Frame_FIFO[i].flag = UNUSED;
	}

	/**********************subprocess_FIFO**********************/
	pid = fork();

	if(pid == -1)		// create process error 
	{
		printf("* creat subprocess_FIFO failed!\n");
		exit(0);
	}
	else if(pid == 0)	// subprocess 
	{
		printf("* subprocess_FIFO %d\n", gtid = getpid());

		while(access_index < sequence_len)
		{
			for(i = 0; i < frame_num; i++)		// check if page exists in memory 
			{	
				if (M_Frame[i].flag == USED)
				{
					if(M_Frame[i].page_no == Access_Series[access_index])
					{
						success_flag = true;	// page exists in memory
						break;
					}
				}
				else							// memory isn't full
					break;
			}

			if(!success_flag)	// page absent/page not exists in memory 
			{
				diseffect += 1.0;

				for(i = 0; i < frame_num; i++)		// check if frames are full 
				{	
					if(M_Frame[i].flag == UNUSED)	// not full 
					{
						M_Frame[i].flag = USED;
						M_Frame[i].page_no = Access_Series[access_index];
						break;
					}
				}

				if(i == frame_num)	// full 
				{
					for(i = 0; i < frame_num - 1; i++)	 
						M_Frame[i].page_no = M_Frame[i + 1].page_no;			 // 栈中元素依次前移
					M_Frame[frame_num - 1].page_no = Access_Series[access_index];// 新元素在栈顶
				}
			}

			printf("requirement for page %d\n", Access_Series[access_index]);
			for(i = frame_num - 1; i >= 0; i--)	// print the state of frames 
			{
				if(M_Frame[i].flag == UNUSED)
					printf("* M_Frame[%d]:  \n",i);
				else
					printf("* M_Frame[%d]: %d\n", i, M_Frame[i].page_no);
			}
			printf("--------------\n");

			success_flag = false;
			access_index++;
		}

		absence_rate = diseffect / sequence_len;	// 缺页率计算
		success_rate = 1 - absence_rate;
		printf("* subprocess_FIFO %d successful [%d]:absence_rate=%f, success_rate=%f\n\n",
			gtid, frame_num, absence_rate, success_rate);

		access_index = 0;
		success_flag = false;
		diseffect = 0.0;
		exit(0);
	}

	reid = wait(NULL);
	if(reid == -1)
		printf("* call subprocess_FIFO failed!\n");

	/**********************subprocess_FIFO_Belady**********************/
	pid = fork();

	if(pid == -1)    // create process error 
	{
		printf("* creat subprocess_FIFO failed!\n");
		exit(0);
	}
	else if(pid == 0)	// subprocess 
	{
		printf("* subprocess_FIFO %d\n", gtid = getpid());

		while(access_index < sequence_len)
		{
			for(i = 0; i < frame_num_FIFO; i++)	// check if page exists in memory or not 
			{	
				if(M_Frame_FIFO[i].flag == USED)
				{
					if(M_Frame_FIFO[i].page_no == Access_Series[access_index])
					{
						success_flag = true;	// page exists in memory 
						break;
					}
				}
				else
					break;
			}

			if(!success_flag)	// page absent/page not exists in memory 
			{
				diseffect += 1.0;

				for(i = 0; i < frame_num_FIFO; i++)	// check if frames are full or not 
				{	
					if(M_Frame_FIFO[i].flag == UNUSED)	// not full 
					{
						M_Frame_FIFO[i].flag = USED;
						M_Frame_FIFO[i].page_no = Access_Series[access_index];
						break;
					}
				}

				if(i == frame_num_FIFO)	// full 
				{
					for(i = 0; i < frame_num_FIFO - 1; i++)	
						M_Frame_FIFO[i].page_no = M_Frame_FIFO[i + 1].page_no;
					M_Frame_FIFO[frame_num_FIFO - 1].page_no = Access_Series[access_index];
				}
			}
			
			printf("requirement for page %d\n", Access_Series[access_index]);
			for(i = frame_num_FIFO - 1; i >= 0; i--)	// print the state of frames 
			{
				if(M_Frame_FIFO[i].flag == UNUSED)
					printf("* M_Frame[%d]:  \n",i);
				else
					printf("* M_Frame[%d]: %d\n", i, M_Frame_FIFO[i].page_no);
			}
			printf("--------------\n");
			success_flag = false;
			access_index++;
		}

		absence_rate = diseffect / sequence_len;
		success_rate = 1 - absence_rate;
		printf("* subprocess_FIFO %d successful [%d]: absence_rate=%f, success_rate=%f\n\n",
			gtid, frame_num_FIFO, absence_rate, success_rate);

		access_index = 0;
		success_flag = false;
		diseffect = 0.0;
		exit(0);
	}

	reid = wait(NULL);
	if(reid == -1)
		printf("* call subprocess_FIFO failed!\n");

	/**********************subprocess_LRU**********************/
	pid = fork();

	if(pid == -1)    	// create process error 
	{
		printf("* creat subprocess_LRU failed!\n");
		exit(0);
	}
	else if(pid == 0)	// subprocess
	{
		printf("* subprocess_LRU %d\n", gtid = getpid());

		while(access_index < sequence_len)
		{
			for(i = 0; i < frame_num; i++)	// check if page exists in memory 
			{	
				if (M_Frame[i].flag == USED)
				{
					if (M_Frame[i].page_no == Access_Series[access_index])
					{
						success_flag = true;	// page exists in memory 

						for(j = i; j < frame_num - 1; j++)	// 将命中的页重新放到栈顶
						{
							if (M_Frame[j + 1].flag == UNUSED)
								break;
							else
							{
								M_Frame[j].page_no = M_Frame[j + 1].page_no;
								M_Frame[j + 1].page_no = Access_Series[access_index];
							}
						}
						break;
					}
				}
				else
					break;	
			}

			if(!success_flag)	// 未命中 
			{
				diseffect += 1.0;

				for(i = 0; i < frame_num; i++)		// check if frames are full 
				{	
					if(M_Frame[i].flag == UNUSED)	// not full 
					{
						M_Frame[i].flag = USED;
						M_Frame[i].page_no = Access_Series[access_index];
						break;
					}
				}

				if(i == frame_num)	// full 
				{
					for(i = 0; i < frame_num - 1; i++)	// 栈底元素出栈，栈顶压入新元素
						M_Frame[i].page_no = M_Frame[i + 1].page_no;
					M_Frame[frame_num - 1].page_no = Access_Series[access_index];
				}
			}

			for(i = frame_num - 1; i >= 0; i--)	// print the state of frames 
			{
				if(M_Frame[i].flag == UNUSED)
					printf("* M_Frame[%d]:  \n",i);
				else
					printf("* M_Frame[%d]: %d\n", i, M_Frame[i].page_no);
			}
			printf("--------------\n");
			success_flag = false;
			access_index++;
		}

		absence_rate = diseffect / sequence_len;
		success_rate = 1 - absence_rate;
		printf("* subprocess_LRU %d successful [%d]: absence_rate=%f, success_rate=%f\n", 
			gtid, frame_num, absence_rate, success_rate);
		exit(0);
	}

	reid = wait(NULL);
	if(reid == -1)
		printf("* call subprocess_LRU failed!\n");

	return 0;
}