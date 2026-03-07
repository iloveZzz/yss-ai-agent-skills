package ${base_package}.repository.gateway.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.yss.cloud.dto.query.PageQuery;
import com.yss.cloud.dto.result.PageResult;
import ${base_package}.domain.${domain_segment}.gateway.${domain_name}Gateway;
import ${base_package}.domain.${domain_segment}.model.${domain_name};
import ${base_package}.repository.${domain_name}Repository;
${convertor_import}
import ${base_package}.repository.entity.${domain_name}PO;
import ${base_package}.repository.util.PageUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Repository
@RequiredArgsConstructor
public class ${domain_name}GatewayImpl implements ${domain_name}Gateway {

    private final ${domain_name}Repository ${repository_field_name};

    @Override
    public ${pk_java_type} create(${domain_name} entity) {
        ${domain_name}PO po = ${to_po_expr};
        ${repository_field_name}.insert(po);
        return po.${pk_getter}();
    }

    @Override
    public boolean updateById(${domain_name} entity) {
        return ${repository_field_name}.updateById(${to_po_expr}) > 0;
    }

    @Override
    public boolean deleteById(${pk_java_type} ${pk_field_name}) {
        return ${repository_field_name}.deleteById(${pk_field_name}) > 0;
    }

    @Override
    public Optional<${domain_name}> findById(${pk_java_type} ${pk_field_name}) {
        return Optional.ofNullable(${repository_field_name}.selectById(${pk_field_name})).map(this::toDomain);
    }

    @Override
    public PageResult<${domain_name}> page(PageQuery query) {
        LambdaQueryWrapper<${domain_name}PO> wrapper = Wrappers.lambdaQuery(${domain_name}PO.class);
${logic_delete_condition}
        wrapper.orderByDesc(${order_by_expr});
        IPage<${domain_name}PO> result = ${repository_field_name}.selectPage(PageUtil.page(query), wrapper);
        List<${domain_name}> records = result.getRecords().stream().map(this::toDomain).collect(Collectors.toList());
        return PageResult.of(records, result.getTotal(), result.getSize(), result.getCurrent());
    }

${mapping_block}
}
