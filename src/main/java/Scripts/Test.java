package Scripts;

import Reader.DocxReader.DocxReader;
import Reader.DocxReader.Rule.impl.SummaryPartRule;
import Reader.DocxReader.SingletonDocxReader;

import java.util.ArrayList;

public class Test {
    public static void main(String[] args) {
        DocxReader reader = SingletonDocxReader.getDocxReader(new SummaryPartRule("2"));
        ArrayList<String> l = new ArrayList<>();
        reader.readDocSplits("C:\\Users\\Administrator\\Desktop\\college\\junior2\\项目实训\\准备阶段\\dataset\\周易经传词汇卷",l);
        System.out.println(l);
    }
}
