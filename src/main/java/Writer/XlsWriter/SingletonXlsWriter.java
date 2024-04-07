package Writer.XlsWriter;

public class SingletonXlsWriter {
    private static XlsWriter xlsWriter = null;

    public synchronized static XlsWriter getXlsWriter(){
        if(xlsWriter==null){
            xlsWriter = new XlsWriter();
        }

        return xlsWriter;
    }
}
