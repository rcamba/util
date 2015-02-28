import java.awt.Robot;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.Canvas;
import java.awt.Graphics;

import java.awt.image.BufferedImage;

import javax.swing.JFrame;

import javax.imageio.*;


import java.io.*;

public class CaptureScreen extends Canvas
{
	Rectangle screenRectangle=new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());

	Robot myRobot;

	BufferedImage screenImage;
	
	
	
	public CaptureScreen()
	{
		try
		{
			myRobot=new Robot();
		}
		catch(Exception exception)
		{
			exception.printStackTrace();
		}

		screenImage=myRobot.createScreenCapture(screenRectangle);

		/*
		JFrame myFrame=new JFrame("Capture Screen");

		myFrame.add(this);

		myFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		myFrame.setSize(Toolkit.getDefaultToolkit().getScreenSize().width,Toolkit.getDefaultToolkit().getScreenSize().height);
		myFrame.setVisible(true);
		*/
		File file = new File("screenshot.png");
		try
		{
			ImageIO.write(screenImage,"png",file);
		}
		catch(Exception exception)
		{
			exception.printStackTrace();
		}
		
		
	}

	public void paint(Graphics g)
	{
		g.drawImage(screenImage,0,0,this);
	}

	public static void main(String[]args)
	{
		CaptureScreen cs=new CaptureScreen();
	}
}
