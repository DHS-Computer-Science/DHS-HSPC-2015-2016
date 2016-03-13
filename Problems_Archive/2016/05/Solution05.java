import java.util.*;
public class Solution05 {
  public static void main(String[] args) throws Exception {
    //Scanner scan = new Scanner(new java.io.File("Input7.txt"));
    Scanner scan = new Scanner(System.in);
    int cases = Integer.parseInt(scan.nextLine());
    for(int c = 0; c < cases; c++) {
      int lines = Integer.parseInt(scan.nextLine());
      String[][] map = new String[lines][1];
      for(int i = 0; i < lines; i++) {
        map[i] = scan.nextLine().toLowerCase().split("");
      }
      int[][] values = new int[map.length][map[0].length];
      boolean[][] used = new boolean[map.length][map[0].length];
      for(int i = 0; i < values.length; i++) {
        for(int j = 0; j < values[i].length; j++) {
          if(map[i][j].equals("x"))
            values[i][j] = -1;
          else
            values[i][j] = -2;
        }
      }
      values[0][values[0].length-1] = 0;
      int l = 1;

      while(values[0][1]==-2) {
        for(int i = 0; i < values.length; i++) {
          for(int j = 0; j < values[i].length; j++) {
            if(values[i][j]==-2&&(
              (i < values.length - 1 && values[i+1][j]>=0 && !used[i+1][j])||
              (i > 0 && values[i-1][j]>=0&& !used[i-1][j])||
              (j < values[i].length - 1 && values[i][j+1]>=0&& !used[i][j+1])||
              (j > 1 && values[i][j-1]>=0&& !used[i][j-1]))) {
                  values[i][j] = l;
                  used[i][j] = true;
            }
          }
        }
        l++;
        for(int i = 0; i < values.length; i++)
          for(int j = 0; j < values[i].length; j++)
            used[i][j] = false;
      }
      int x = 0;
      int y = 1;
      int d = values[0][1]-1;
      String solution = "";
      for(int i = 0; i < values[0][1]; i++) {
        if(x + 1 < values.length && values[x+1][y]==d) {
          x++;
          solution+="D";
        }
        else if(x > 0 && values[x-1][y]==d) {
          x--;
          solution+="U";
        }
        else if(y < values[x].length-1 && values[x][y+1]==d) {
          y++;
          solution+="R";
        }
        else if(y > 0 && values[x][y-1]==d) {
          y--;
          solution+="L";
        }
        d--;
      }
      System.out.println("Case "+ (c+1) +": "+ solution);
    }
  }
  public static boolean print(int num) {
    //System.out.println(num);
    return(true);
  }
}
