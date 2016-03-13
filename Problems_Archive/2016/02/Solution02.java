import java.util.*;

public class Solution02 {
  public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);
    int times = scan.nextInt();
    for(int j = 0; j < times; j++) {
      int nNum = scan.nextInt();
      double[] array = new double[nNum];
      double average = 0;
      for(int i = 0; i < nNum; i++) {
        array[i] = scan.nextDouble();
        average += array[i];
      }
      average /= array.length;
      Arrays.sort(array);
      double median;
      if(nNum % 2 == 0)
        median = (array[(nNum/2)-1] + array[nNum/2]) / 2.0;
      else
        median = array[nNum/2];
      double sum = 0;
      for(int i = 0; i < nNum; i++)
        sum += Math.pow(array[i] - average, 3);
      boolean negative = false;
      if(sum/median < 0)
        negative = true;
      double solution = Math.pow(Math.abs(sum/median), 1/5.0);
      if(negative)
        solution *= -1;
      System.out.printf("Case %d: %.2f\n", j+1, solution);
    }
  }
}