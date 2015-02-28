class LinkedList
{
	private Node head;
	private int size=0;
	
	public LinkedList()
	{
		head= null;
	}
	
	public int size()
	{
		return size;
	}
	
	public boolean isEmpty()
	{
		boolean result=false;
		if (head==null)
			result=true;
		
		return result;
	}
	
	public Node find(Object theItem) 
	{
		//(return a reference to this item in the list if found, otherwise return null)
		
		Node curr, result=null;
		boolean found=false;
		
	
		curr=head;
		while (curr!=null && found==false)
		{
			
			if(curr.getData()==theItem)
			{
				result=curr;
				found=true;// end loop
			}
			
			else
				curr=curr.getNext();
				
		}
		
		return result;
	}
	
	
	public boolean insert(Object theItem)
	{
		//if item is not currently in the list, insert it at the beginning of the list and return true; otherwise make no change to the list and return false)
		Node curr, temp;
		boolean success=false;
		
		
		
		if(head==null)
		{
			head=new Node(theItem);
			success=true;
			size++;
		}
		
		else 
		{
			temp=new Node(theItem);
			temp.setNext(head);
			head=temp;
			success=true;
			size++;
			/*
			if (find(theItem)==null)
			{
				temp=new Node(theItem);
				temp.setNext(head);
				head=temp;
				success=true;
				size++;
			}
			
			else
				System.out.println("\nError: The item that you are trying to insert is already in the list");
			*/
		}
		
		return success;
	}
	
	public boolean delete(Object theItem) 
	{
		//(if this item is currently in the list, delete it and return true; otherwise make no change to the list and return false)
		Node curr, prev;
		boolean result=true, found=false;
		

		if(head.getData()==theItem)
		{
			head=head.getNext();
			found=true;
			size--;
			
		}	
		
		
		else
		{
			curr=head.getNext();
			prev=head;
			
			while(curr!=null && found==false)
			{
				
				if(curr.getData()==theItem)
				{
					prev.setNext(curr.getNext());
					size--;
					found=true;
				
				}
				
				prev=curr;
				curr=curr.getNext();
				
			}
			
		}
		
		if (found==false)
		{
			System.out.println("\nThe item that you are trying to delete is not in the list.");
			result=false;
		}
		
		return result;
	}
	
	public Object getItem(int position)
	{
		//starts at 0 for first item
		//returns the Node in given position
		Node curr;
		Object result=null;;
		
		
		int counter=0;
		
		if ((position)<size)
		{
			curr=head;
			while (curr!=null && counter<=position)
			{
				
				if(counter==position)
				{
					result=curr.getData();
					counter=position;// end loop
				}
				
				else
				{
					curr=curr.getNext();
				}
				counter++;
			}
		}
		
		else
			System.out.println("Out of bounds. Position argument is greater than size.");
		
		return result;
	}
	
	
	
	public String toString()
	{
		String resultString="";
		Node curr=head;
		while (curr!=null)
		{
			
			resultString=resultString+curr.getData()+"\n";
			curr=curr.getNext();
			
		}
		if (resultString.length()>0)
			resultString=(resultString.substring(0,resultString.length()-1));//removes the last "\n"
		
		
		
		return resultString;
	}
	
}