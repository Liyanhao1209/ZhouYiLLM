package Scripts;

import Reader.DocxReader.DocxReader;
import Reader.DocxReader.Rule.impl.DummyRule;
import Reader.DocxReader.SingletonDocxReader;

import java.util.List;

public class Test {
    public static void main(String[] args) {
        DocxReader reader = SingletonDocxReader.getDocxReader(new DummyRule());
        List<String> l = reader.readDoc("C:\\Users\\Administrator\\Desktop\\college\\junior2\\项目实训\\准备阶段\\dataset\\周易经传词汇卷\\87-126.docx");
        System.out.println(l);
    }
}
