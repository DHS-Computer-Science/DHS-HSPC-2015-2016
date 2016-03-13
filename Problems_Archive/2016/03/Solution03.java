import java.util.Scanner;

public class Solution03 {
  public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);
    int cases = Integer.parseInt(scan.nextLine());
    for(int c = 0; c < cases; c++) {
      long number = scan.nextLong();
      int count = 0;
      for(int i = 2; i <= Math.sqrt(number); i++) {
        int temp = 0;
        while((number%i) == 0) {
          number /= i;
          temp++;
        }
        if(temp > 1)
          count+=temp;
      }
      System.out.printf("Case %d: %d\n", c+1, count);
    }
  }
}
