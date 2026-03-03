package com.yss.quality.repository.gateway.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.yss.cloud.dto.result.PageResult;
import com.yss.quality.client.dto.query.QualityTemplatePage;
import com.yss.quality.client.vo.QualityTemplateVO;
import com.yss.quality.domain.template.gateway.QualityTemplateGateway;
import com.yss.quality.repository.QualityTemplateRepository;
import com.yss.quality.repository.convertor.QualityTemplateConvertor;
import com.yss.quality.repository.entity.QualityTemplatePO;
import com.yss.quality.repository.util.PageUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;
import org.springframework.util.StringUtils;

import java.util.List;

@Repository
@RequiredArgsConstructor
public class QualityTemplateGatewayImpl implements QualityTemplateGateway {
    private final QualityTemplateRepository qualityTemplateRepository;

    @Override
    public PageResult<QualityTemplateVO> pageQualityTemplate(QualityTemplatePage query) {
        LambdaQueryWrapper<QualityTemplatePO> wrapper = Wrappers.lambdaQuery(QualityTemplatePO.class);
        if (StringUtils.hasText(query.getTemplateName())) {
            wrapper.like(QualityTemplatePO::getTemplateName, query.getTemplateName());
        }
        wrapper.orderByDesc(QualityTemplatePO::getCreatedDate);
        IPage<QualityTemplatePO> result = qualityTemplateRepository.selectPage(PageUtil.page(query), wrapper);
        List<QualityTemplateVO> records = QualityTemplateConvertor.INSTANCE.toQualityTemplateVOList(result.getRecords());
        return PageResult.of(records, result.getTotal(), result.getSize(), result.getCurrent());
    }
}
