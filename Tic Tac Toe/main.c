/*
    // Tic Tac Toe Game 3 by 3
    // Enter row index then column index  that you would want to play into standard input.
    // Indexes start
    // GOodluck

*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define SQUARE_LEN (3)



char arr[100]= "   |   |   \n-----------\n   |   |   \n-----------\n   |   |   \n";
bool entries [SQUARE_LEN][SQUARE_LEN] = {false};
int sums[8] = {0};
int turn =0;

void print_arr(int * , int );
void till_good_input(int * , int *);
bool has_player_won(int , int);
void draw_curr_state(int ,int  , char );
void update_sum_array(int , int , int);
int input_not_valid(int , int);


int main()
{
    /*
    Start player plays
    Verify if entry hasnt already been entered (use loop till user puts a valid entry) (First test that it matches integers
    Update the sums array accordingly
    Draw the current state
    verify if curr player has won and break
    if player didnt win continue loop , switch the status results

    */

    int row_chosen = 1, col_chosen = 1,status;
    int times =0;
    bool has_won;

    while((has_won = !has_player_won(row_chosen,col_chosen))){


        if(times == SQUARE_LEN*SQUARE_LEN)
            break;
        printf("Player %c Turn\n", turn ? 'B' : 'A');
        test : till_good_input(&row_chosen,&col_chosen);


        status = input_not_valid(row_chosen , col_chosen);


        switch(status){

        case 1:
            printf("Your entry was invalid. Put another stuff\n");
            goto test;
        case -1:
            printf("Cell already taken\n");
            goto test;
            break;

        }

        entries[row_chosen - 1][col_chosen - 1] = true ;// Make that pos become filled
        update_sum_array(row_chosen,col_chosen,turn);
        draw_curr_state(row_chosen,col_chosen, turn % 2 ? 'O' : 'X');
        printf("\n\n\n");
        turn = 1 - turn; // toggle between 1 and 0;
        times ++;
    }
    if(!has_won)
        printf("Player %c Wins!!\n", turn ? 'A' : 'B');
    else
        printf("It ended in a Draw\n");

    printf("Thanks for Playing my game. Goodbye!!\n");
    return 0;

}


void till_good_input(int * row, int* col){
    while(scanf("%d %d",row,col) !=2){
          scanf("%*s");
    }
}


int input_not_valid(int row , int column){

    if(entries[row-1][column-1])
        return -1;
    else if (row < 1 || row >3 || column < 0 || column > 3){
        return 1;
    }
    return 0;

}

void update_sum_array(int row,int col,int turn){
    int num = turn ? -1 : 1;
    sums[row - 1]+=num;
    sums[3 + col -1]+=num;

    if(row == col)
        sums[6]+=num;
    if (row + col == 4)
        sums[7]+=num;

    print_arr(sums,8);
}

void print_arr(int * arr, int len){

    while(len){
        printf("%d  ",*arr);
        arr++;
        len--;
    }

    printf("\n");

}


void draw_curr_state(int row,int column , char ch){
    int pos = 24 *(row - 1) +4 * (column - 1) + 1;
    arr[pos] = ch;
    printf("\n\n\n");
    printf(arr);
}

bool has_player_won(int row, int col){
    bool ans = false;

    if(row == col)
        ans = ans ||(sums[6] == 3 || sums[6] == -3);
    if(row + col == 4)
        ans = ans || (sums[7] == 3 || sums[7] == -3);

    return ans || (sums[row -1] == 3 || sums[row -1] == -3 ) || (sums[3 + col -1] == 3 || sums[3 + col -1] == -3);
}





