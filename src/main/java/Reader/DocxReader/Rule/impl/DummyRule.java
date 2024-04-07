package Reader.DocxReader.Rule.impl;

import Reader.DocxReader.Rule.Interface.ReadRule;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.util.List;

public class DummyRule implements ReadRule {
    @Override
    public void addParagraph(XWPFParagraph paragraph, List<String> res) {
        res.add(paragraph.getText());
    }
}
