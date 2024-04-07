package Reader.DocxReader.Rule.impl;

import Reader.DocxReader.Rule.Interface.ReadRule;
import org.apache.commons.math3.stat.descriptive.summary.Sum;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.util.List;

public class SummaryPartRule implements ReadRule {
    String splitStyle;
    public SummaryPartRule(String split){
        this.splitStyle = split;
    }

    @Override
    public void addParagraph(XWPFParagraph paragraph, List<String> res) {
        String style = paragraph.getStyle();
        System.out.println(style);

        if(paragraph.getText().isEmpty()){
            return;
        }
        if(style!=null&&style.equals(splitStyle)){
            res.add(paragraph.getText());
            res.add("");
        }else{
            res.set(res.size()-1,res.get(res.size()-1)+paragraph.getText());
        }
    }
}
