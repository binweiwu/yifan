package com.git.test;

public class test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		char c = 'A';
		System.out.println((int)c);
		int lines = 10;
		for (int i=0; i<= lines; i++) {
			for (int j=0; j<lines-i; j++) {
				System.out.print("*");
			}
			for (int k=0; k<i; k++) {
				System.out.print(" ");
			}
			System.out.println();
		}
		

	}

}
