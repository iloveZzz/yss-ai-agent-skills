package ${base_package}.repository.gateway.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.yss.cloud.dto.result.PageResult;
import ${base_package}.client.dto.query.${domain_name}Page;
import ${base_package}.client.vo.${domain_name}VO;
import ${gateway_interface_fqn};
import ${base_package}.repository.${domain_name}Repository;
import ${base_package}.repository.convertor.${domain_name}Convertor;
import ${base_package}.repository.entity.${domain_name}PO;
import ${base_package}.repository.util.PageUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@RequiredArgsConstructor
public class ${domain_name}GatewayImpl implements ${gateway_interface_name} {

    private final ${domain_name}Repository ${repository_field_name};

    @Override
    public PageResult<${domain_name}VO> page${domain_name}(${domain_name}Page query) {
        LambdaQueryWrapper<${domain_name}PO> wrapper = Wrappers.lambdaQuery(${domain_name}PO.class);
        wrapper.orderByDesc(${domain_name}PO::getCreatedDate);
        IPage<${domain_name}PO> result = ${repository_field_name}.selectPage(PageUtil.page(query), wrapper);
        List<${domain_name}VO> records = ${domain_name}Convertor.INSTANCE.toVOList(result.getRecords());
        return PageResult.of(records, result.getTotal(), result.getSize(), result.getCurrent());
    }
}
