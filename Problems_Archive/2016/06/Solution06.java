import java.util.*;

public class Solution06 {
  static class LinkStack<T> {
    private Num<T> topp;

    public LinkStack() {
      this.topp = null;
    }

    public boolean empty() {
      return this.topp == null;
    }

    public void push(T value) {
      if(this.empty())
        this.topp = new Num<T>(value);
      else {
        Num<T> tmp = new Num<T>(value);
        this.topp.setNext(tmp);
        tmp.setPrev(this.topp);
        this.topp = tmp;
      }
    }

    public T pop() {
      if(this.topp.getPrev() != null)
        this.topp.getPrev().setNext(null);
      Num<T> tmp = this.topp;
      this.topp = this.topp.getPrev();
      return tmp.getValue();
    }

    public T peek() {
      return this.topp.getValue();
    }
  }

  static class Num<T> {
    private T      value;
    private Num<T> next;
    private Num<T> prev;

    public Num() {
      this.value = null;
      this.next  = null;
      this.prev  = null;
    }

    public Num(T value) {
      this.value = value;
      this.next  = null;
      this.prev  = null;
    }

    public void setNext(Num<T> next) {
      this.next = next;
    }

    public Num<T> getNext() {
      return this.next;
    }

    public void setPrev(Num<T> prev) {
      this.prev = prev;
    }

    public Num<T> getPrev() {
      return this.prev;
    }

    public void setValue(T value) {
      this.value = value;
    }

    public T getValue() {
      return this.value;
    }
  }

  public static boolean isNum(String s) {
    return s.matches("[+-]?[0123456789\\.]*");
  }

  public static boolean isOpperator(String s) {
    return "+-*/%|&x^sctbdoiuygkflnrmj".indexOf(s) != -1;
  }

  public static void solve(LinkStack<Double> stack, String opperation) {
    double tmp;
    switch(opperation.charAt(0)){
      case '+':
        stack.push(stack.pop()+stack.pop());
        break;
      case '-':
        tmp = stack.pop();
        stack.push(stack.pop()-tmp);
        break;
      case '*':
        stack.push(stack.pop()*stack.pop());
        break;
      case '/':
        tmp = stack.pop();
        stack.push(stack.pop()/tmp);
        break;
      case '^':
        tmp = stack.pop();
        double num = stack.pop();
        if(num < 0 && ((int)(Math.pow(tmp, -1))%2 != 0 ||
          (Math.pow(tmp, -1)-(int)(Math.pow(tmp, -1))) > 0.0001)) {
            if((tmp-(int)tmp) < 0.0001 && (int)tmp%2 == 0)
              stack.push(Math.pow(Math.abs(num), tmp));
            else
              stack.push(-1*Math.pow(Math.abs(num), tmp));
         }
         else
           stack.push(Math.pow(num, tmp));
         break;
      case '|':
        stack.push(Math.sqrt(stack.pop()));
        break;
    }
  }

  public static double postfixSolve(String[] expression) {
    LinkStack<Double> stack = new LinkStack<Double>();
    for(String item : expression) {
      if(isOpperator(item))
        solve(stack, item);
      else
        stack.push(Double.valueOf(item).doubleValue());
    }
    return stack.pop();
  }

  public static String[] splitExpression(String expression) {
    if(expression.length() < 2) {
      return new String[] {expression};
    }

    int nIndexA = 0;
    int nIndexB = 0;

    java.util.ArrayList<String> list = new java.util.ArrayList<String>();
    while(nIndexB < expression.length()) {
      while(isNum(expression.substring(nIndexA, ++nIndexB))
            && nIndexB < expression.length());
      if(!isNum(expression.substring(nIndexA, nIndexB)))
        nIndexB--;
      list.add(expression.substring(nIndexA, nIndexB));
      if(nIndexB < expression.length())
        list.add(expression.substring(nIndexB++, nIndexB));
      while(nIndexB < expression.length() &&
            list.get(list.size()-1).equals(")")) {
        list.add(expression.substring(nIndexB++, nIndexB));
      }
      nIndexA=nIndexB;
    }
    list.removeAll(Arrays.asList("", null));
    return list.toArray(new String[list.size()]);
  }

  //return whether op1 has lower precedence than op2
  private static boolean lowerPrecedence(String op1, String op2) {
      int p1;
      int p2;

      if("(".equals(op1))
        p1 = 7;
      else if("|".indexOf(op1) != -1)
        p1 = 0;
      else if("^".indexOf(op1) != -1)
        p1 = 1;
      else if("*/%".indexOf(op1) != -1)
        p1 = 2;
      else if("+-".indexOf(op1) != -1)
        p1 = 3;
      else
        p1 = "r&x".indexOf(op1)+4;

      if("(".equals(op2))
        p2 = 7;
      else if("|".indexOf(op2) != -1)
        p2 = 0;
      else if("^".indexOf(op2) != -1)
        p2 = 1;
      else if("*/%".indexOf(op2) != -1)
        p2 = 2;
      else if("+-".indexOf(op2) != -1)
        p2 = 3;
      else
        p2 = "r&x".indexOf(op2)+4;

      return p1 > p2;
   }

  public static String[] infixToPostfix(String[] expression) {
    LinkStack<String> operators = new LinkStack<String>();
    java.util.ArrayList<String> postfix = new java.util.ArrayList<String>();

    for(String item : expression) {
      if(item.equals("("))
        operators.push(item);
      else if(item.equals(")")) {
        String operator;
        while(!operators.empty() && !(operator = operators.pop()).equals("(")) {
          postfix.add(operator);
        }
      }
      else if(isOpperator(item)) {
        while(!operators.empty() &&
              !lowerPrecedence((operators.peek()), item)) {
          if(operators.peek().equals("("))
            operators.pop();
          else
            postfix.add(operators.pop());
        }
        operators.push(item);
      }
      else {
        postfix.add(item);
      }
    }
    while(!operators.empty())
      postfix.add(operators.pop());
    return postfix.toArray(new String[postfix.size()]);
  }

  public static double evaluate(String expression) {
    expression = expression.replaceAll("\\s+", "");
    expression = expression.replace("sqrt", "|");
    return postfixSolve(infixToPostfix(splitExpression(expression)));
  }

  public static void main(String[] args) throws java.io.IOException {
    java.io.BufferedReader input
         = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
    int nCases = Integer.valueOf(input.readLine());
    for(int i=1; i<=nCases; i++) {
      String expression = input.readLine();
      System.out.printf("Case %d: %.3f\n", i, evaluate(expression));
    }

    //close stream
    input.close();
  }
}
