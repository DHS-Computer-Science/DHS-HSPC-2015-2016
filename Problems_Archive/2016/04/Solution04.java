import java.util.Scanner;

public class Solution04 {
  public static String reverse(String in) {
    return new StringBuilder(in).reverse().toString();
  }
  public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);
    int nCases = scan.nextInt(); scan.nextLine();
    for(int k = 1; k <= nCases; k++) {
      String phrase = scan.nextLine();
      String[] brokenPhrase = phrase.split(" ");
      int stop = brokenPhrase.length;
      for(int i = 0; i < brokenPhrase.length; i++) {
        if(brokenPhrase[i].equals("stop")) {
          stop = i;
          break;
        }
      }
      for(int i = 0; i < stop; i++) {
        if(brokenPhrase[i].equals("invert")) {
          int j = i + 1;
          while(j < stop) {
            if(!brokenPhrase[j].equals("invert") &&
               !brokenPhrase[j].equals("reverse") &&
               !brokenPhrase[j].equals("fuse") &&
               !brokenPhrase[j].equals("tunnel") &&
               !brokenPhrase[j].equals("")) {
              brokenPhrase[j] = reverse(brokenPhrase[j]);
              break;
            }
            else
              j++;
          }
          brokenPhrase[i] = "";
        }
        if(brokenPhrase[i].equals("reverse")) {
          int j = i - 1;
          while(j >= 0) {
            if(!brokenPhrase[j].equals("invert") &&
               !brokenPhrase[j].equals("reverse") &&
               !brokenPhrase[j].equals("fuse") &&
               !brokenPhrase[j].equals("tunnel") &&
               !brokenPhrase[j].equals("")) {
              brokenPhrase[j] = reverse(brokenPhrase[j]);
              break;
            }
            else
              j--;
          }
          brokenPhrase[i] = "";
        }
        if(brokenPhrase[i].equals("fuse")) {
          int j = i + 1;
          int count = 0;
          int firstWordIndex = -1;
          String firstWord = null;
          String secondWord = null;
          while(j < stop && count < 2) {
            if(!brokenPhrase[j].equals("invert") &&
               !brokenPhrase[j].equals("reverse") &&
               !brokenPhrase[j].equals("fuse") &&
               !brokenPhrase[j].equals("tunnel") &&
               !brokenPhrase[j].equals("")) {
              if(firstWordIndex < 0) {
                firstWordIndex = j;
                firstWord = brokenPhrase[j];
              }
              else {
                secondWord = brokenPhrase[j];
                brokenPhrase[j] = "";
                break;
              }
              brokenPhrase[j] = "";
            }
            j++;
          }
          if(secondWord != null)
            brokenPhrase[firstWordIndex] = firstWord + secondWord;
          brokenPhrase[i] = "";
        }
        if(brokenPhrase[i].equals("tunnel")) {
          int j = i + 1;
          String firstWord = null;
          int firstIndex = -1;
          String secondWord = null;
          int secondIndex = -1;
          while(j < stop) {
            if(!brokenPhrase[j].equals("invert") &&
               !brokenPhrase[j].equals("reverse") &&
               !brokenPhrase[j].equals("fuse") &&
               !brokenPhrase[j].equals("tunnel") &&
               !brokenPhrase[j].equals("") && secondIndex < 0) {
              secondWord = brokenPhrase[j];
              secondIndex = j;
            }
            j++;
          }
          j = i - 1;
          while(j >= 0) {
            if(firstWord == null && !brokenPhrase[j].equals("invert")
                                 && !brokenPhrase[j].equals("reverse")
                                 && !brokenPhrase[j].equals("fuse")
                                 && !brokenPhrase[j].equals("tunnel")
                                 && !brokenPhrase[j].equals("")) {
              firstWord = brokenPhrase[j];
              firstIndex = j;
            }
            j--;
          }
          if(firstWord != null && secondWord != null) {
            brokenPhrase[secondIndex] = firstWord;
            brokenPhrase[firstIndex] = secondWord;
          }
          brokenPhrase[i] = "";
        }
      }
      System.out.print("Case "+ k +":");
      for(int i = 0; i < stop; i++) {
        if(!brokenPhrase[i].equals(""))
          System.out.print(" "+ brokenPhrase[i]);
      }
      System.out.println();
    }
  }
}