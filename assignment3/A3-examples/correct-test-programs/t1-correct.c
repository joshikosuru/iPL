void main()
{
	int *a,*b, e, f;
   
        a = &e;
        b = &f;

	if (*a >= - *b && -(*a + *b) > 5)
	{
		*a = *a+1;
		if(*a >4)
		*b = *b+1;
	}
}
