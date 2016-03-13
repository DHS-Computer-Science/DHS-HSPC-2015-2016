import java.util.Scanner;
public class Solution01 {
  public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);
    int cases = Integer.parseInt(scan.nextLine());
    for(int i = 1; i <= cases; i++) {
      String parseMe = scan.nextLine();
      System.out.print("Case "+i+": ");
      int totalLength = parseMe.length();
      int totalRemoved = 0;
      parseMe = parseMe.replaceAll("[aeiouAEIOU]","");
      System.out.print(totalLength - parseMe.length()+", ");
      totalLength = parseMe.length();
      parseMe = parseMe.replaceAll("[bcdefghjklmnpqrstvwxzBCDEFGHJKLMNPQRSTVWXZ]","");
      System.out.print(totalLength - parseMe.length()+", ");
      totalLength = parseMe.length();
      parseMe = parseMe.replaceAll("y","");
      System.out.print(totalLength - parseMe.length()+", ");
      totalLength = parseMe.length();
      parseMe = parseMe.replaceAll(" ","");
      System.out.print(totalLength - parseMe.length()+", ");
      totalLength = parseMe.length();
      parseMe = parseMe.replaceAll("[0123456789]","");
      System.out.print(totalLength - parseMe.length()+", ");
      totalLength = parseMe.length();
      System.out.println(totalLength);
    }
  }
}
