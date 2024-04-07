package Reader.DocxReader;

import Reader.DocxReader.Rule.Interface.ReadRule;

public class SingletonDocxReader {
    private static DocxReader docxReader = null;

    public synchronized static DocxReader getDocxReader(ReadRule rule){
        if(docxReader == null){
            docxReader = new DocxReader(rule);
        }else{
            docxReader.rule = rule;
        }

        return docxReader;
    }
}
