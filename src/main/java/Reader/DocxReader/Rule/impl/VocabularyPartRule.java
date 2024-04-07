package Reader.DocxReader.Rule.impl;

import Reader.DocxReader.Rule.Interface.ReadRule;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.util.List;

public class VocabularyPartRule implements ReadRule {
    private final String[] splits = new String[]{"*","+"};
    @Override
    public void addParagraph(XWPFParagraph paragraph, List<String> res) {
        String text = paragraph.getText();
        if(text.isEmpty()){
            return;
        }

        if(isQuestion(text)){
            res.add(text.substring(1));
            res.add("");
        }else{
            res.set(res.size()-1,res.get(res.size()-1)+text);
        }

    }

    private boolean isQuestion(String text){
        for (String split : splits) {
            if(text.startsWith(split)){
                return true;
            }
        }

        return false;
    }
}
